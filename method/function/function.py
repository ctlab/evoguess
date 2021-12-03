from typing import Tuple, Dict, Iterable, Callable

from ..solver.types import Solver
from structure.array import Backdoor
from concurrency.concurrency import Task

Job = Tuple[Callable, Iterable[Task]]
Result = Tuple[Dict[bool, int], Dict[str, int]]
Case = Tuple[int, int, bool, Dict[str, int], Tuple[float, float]]

BASIS = 8


def to_bits(number):
    assert number < 1 << BASIS
    return [1 if number & (1 << (BASIS - i - 1)) else 0 for i in range(BASIS)]


def to_number(bits):
    assert len(bits) <= BASIS
    return sum([1 << (BASIS - i - 1) for i, bit in enumerate(bits) if bit])


def encode_bits(bits):
    data = []
    for array in bits:
        numbers = []
        for i in range(0, len(array), BASIS):
            numbers.append(to_number(array[i:i + BASIS]))
        data.append(bytes(numbers))
    # print('encode_bits: ', bits, ' to ', data)
    return tuple(data)


def decode_bits(data):
    bits = []
    for numbers in data:
        array = []
        for number in numbers:
            array.extend(to_bits(number))
        bits.append(array)
    # print('decode_bits: ', data, ' to ', bits)
    return bits


def encode_result(result):
    if 'learned_literals' in result[3]:
        return result[0], result[1], result[2], result[3]['restarts'], result[3]['conflicts'], result[3]['decisions'], \
               result[3]['propagations'], result[3]['time'], result[4][0], result[4][1], result[3]['learned_literals']
    else:
        return result[0], result[1], result[2], result[3]['restarts'], result[3]['conflicts'], result[3]['decisions'], \
               result[3]['propagations'], result[3]['time'], result[4][0], result[4][1]


def decode_result(data):
    stats = {
        'restarts': data[3],
        'conflicts': data[4],
        'decisions': data[5],
        'propagations': data[6],
        'time': data[7],
    }
    if len(data) > 10:
        stats['learned_literals'] = data[10]
    return data[0], data[1], data[2], stats, (data[8], data[9])


def save_apply(f, arg):
    return None if arg is None else f(arg)


class Function:
    type = None
    name = 'Function'

    def __init__(self,
                 solver: Solver,
                 instance,
                 measure,
                 *args, **kwargs
                 ):
        self.solver = solver
        self.measure = measure
        self.instance = instance

    def get_job(self, backdoor: Backdoor, *dimension, **kwargs) -> Job:
        raise NotImplementedError

    def calculate(self, backdoor: Backdoor, *cases: Case) -> Result:
        raise NotImplementedError

    def decode_results(self, *results: Tuple) -> Iterable[Case]:
        return [save_apply(decode_result, result) for result in results]

    def get_values(self, *cases: Case) -> Iterable[float]:
        return [save_apply(lambda x: self.measure.get(x[3]), case) for case in cases]

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.solver,
            self.measure,
            self.instance
        ]))


__all__ = [
    'Job',
    'Case',
    'Result',
    'Iterable',
    'Backdoor',
    'Function',
    # utils
    'save_apply',
    'encode_bits',
    'decode_bits',
    'encode_result',
    'decode_result'
]
