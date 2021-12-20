from typing import Optional, ParamSpec
from collections.abc import Callable

from instance.impl.instance import Instance
from function.module.solver.solver import Solver
from function.module.measure.measure import Measure

from util.array import concat, slice_by_size
from util.numeral import base_to_binary2, binary_to_base2

ProcessId = int
ProcessTime = float

TaskIndex = int
TaskTime = float
TaskValue = float
TaskStatus = Optional[bool]

Tasks = list[TaskIndex]
Payload = tuple[
    Solver,
    Measure,
    Instance,  # instance = cnf
    # BackdoorBits, # todo: create BackdoorBits
    # todo: parse cnf intervals in process runtime
]

Result = tuple[
    ProcessId,
    ProcessTime,
    TaskIndex,
    TaskTime,
    TaskValue,
    TaskStatus
]

WorkerCallable = Callable[
    [Tasks, Payload],
    list[Result]
]

BASIS = 8

[
    PERMUTATION,
    NUMBERS
] = range(2)


def to_bits(number, basis=BASIS):
    assert number < 1 << basis
    return base_to_binary2(basis, number)


def to_number(bits, basis=BASIS):
    assert len(bits) <= basis
    return binary_to_base2(basis, bits)


def encode_bits(bits):
    return bytes([to_number(chunk) for chunk in slice_by_size(BASIS, bits)])


def decode_bits(data):
    return concat(*(to_bits(number) for number in data))


def decimal_to_base(number, bases):
    values = []
    for base in bases[::-1]:
        number, value = divmod(number, base)
        values.insert(0, value)
    return values


def map_values(values, mappers):
    return [mappers[i][value] for i, value in enumerate(values)]


class Function:
    type = None
    slug = 'function'
    name = 'Function'

    def __init__(self, solver, measure, *args, **kwargs):
        self.solver = solver
        self.measure = measure

    def get_function(self) -> WorkerCallable:
        raise NotImplementedError

    def prepare_data(self, instance, backdoor, dim_type):
        raise NotImplementedError

    def calculate(self, backdoor, *cases):
        raise NotImplementedError

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
    # bits
    'to_bits',
    'to_number',
    'encode_bits',
    'decode_bits',
    # dimension
    'NUMBERS',
    'PERMUTATION',
    'map_values',
    'decimal_to_base',
]
