import json

from typing import Any
from time import time as now

from ..abc import Logger
from ..abc.output import LogFormat

from core.model.point import Vector
from typings.work_path import WorkPath


class VectorDiff(Logger):
    slug = 'logger:vector-diff'

    def __init__(self, out_path: WorkPath, log_format: LogFormat = LogFormat.JSON_LINE):
        super().__init__(out_path, log_format)
        self.last_vector = None

    def write(self, vector: Vector, **kwargs: Any) -> 'Logger':
        if self.last_vector is None:
            points = {'insert': self.last_vector}
        else:
            # todo: get diff
            points = {}

        self.last_vector = vector
        # todo: move object formatting to Logger.write
        return self._write(json.dumps({
            **kwargs, **points,
            'stamp': now() - self.session_enter,
        }), filename='log.jsonl')


__all__ = [
    'VectorDiff'
]
