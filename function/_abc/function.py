from util.array import concat, chunk_slice

BASIS = 8


def to_bits(number):
    assert number < 1 << BASIS
    return [1 if number & (1 << (BASIS - i - 1)) else 0 for i in range(BASIS)]


def to_number(bits):
    assert len(bits) <= BASIS
    return sum([1 << (BASIS - i - 1) for i, bit in enumerate(bits) if bit])


def encode_bits(bits):
    return tuple([
        bytes([
            to_number(chunk)
            for chunk in chunk_slice(BASIS, array)
        ]) for array in bits
    ])


def decode_bits(data):
    return [
        concat(*[
            to_bits(number)
            for number in numbers
        ]) for numbers in data
    ]


def struct_result(data):
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


def destruct_result(result):
    if 'learned_literals' in result[3]:
        return result[0], result[1], result[2], result[3]['restarts'], result[3]['conflicts'], result[3]['decisions'], \
               result[3]['propagations'], result[3]['time'], result[4][0], result[4][1], result[3]['learned_literals']
    else:
        return result[0], result[1], result[2], result[3]['restarts'], result[3]['conflicts'], result[3]['decisions'], \
               result[3]['propagations'], result[3]['time'], result[4][0], result[4][1]


def save_apply(f, arg):
    return None if arg is None else f(arg)


class Function:
    type = None
    slug = 'function'
    name = 'Function'

    def __init__(self, solver, measure, *args, **kwargs):
        self.solver = solver
        self.measure = measure

    def get_function(self):
        raise NotImplementedError

    def prepare_tasks(self, instance, backdoor, *dimension, **kwargs):
        raise NotImplementedError

    def calculate(self, backdoor, *cases):
        raise NotImplementedError

    def struct_results(self, *results):
        return [save_apply(struct_result, result) for result in results]

    def get_values(self, *cases):
        return [save_apply(lambda x: self.measure.get(x[3]), case) for case in cases]

    def __str__(self):
        return self.name

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'solver': self.solver.__info__(),
            'measure': self.measure.__info__(),
        }


__all__ = [
    'Function',
    # util
    'save_apply',
    'encode_bits',
    'decode_bits',
    'struct_result',
    'destruct_result'
]
