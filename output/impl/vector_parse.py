import json
from base64 import b85decode
from typing import Any, Dict, Iterable

from ..abc import Parser

from core.model.point import Point
from core.module.comparator import MinValueMaxSize
from instance.module.variables import Backdoor, variables_from

stub_comparator = MinValueMaxSize()


def deserialize(backdoor: Backdoor, point: Dict[str, Any]) -> Point:
    mask = Backdoor.unpack(b85decode(point['backdoor']))
    return Point(
        backdoor=backdoor.get_copy(mask),
        comparator=stub_comparator
    ).set(**point['estimation'])


class VectorParser(Parser):
    slug = 'parser:vector-parse'

    def parse(self, *args, **kwargs) -> Iterable[Any]:
        backdoor = variables_from(self.var_set())
        for data in map(json.loads, self.read(filename='log.jsonl')):
            yield {**data, 'points': [
                deserialize(backdoor, point) for point in data['points']
            ]}


__all__ = [
    'VectorParser'
]
