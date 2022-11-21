import json

from typing import Any, Dict
from base64 import b85encode
from time import time as now

from ..abc import Logger

from core.model.point import Vector, Point


def serialize(point: Point) -> Dict[str, Any]:
    return {
        'estimation': point.estimation,
        'backdoor': b85encode(point.backdoor.pack()).decode("utf-8"),
    }


class VectorFull(Logger):
    slug = 'logger:vector-full'

    def write(self, vector: Vector, **kwargs: Any) -> 'Logger':
        # todo: move object formatting to Logger.write
        return self._write(json.dumps({
            **kwargs, 'points': [serialize(p) for p in vector],
            'stamp': now() - self.session_enter,
        }), filename='log.jsonl')


__all__ = [
    'VectorFull'
]
