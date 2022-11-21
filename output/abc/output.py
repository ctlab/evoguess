from enum import Enum
from typing import Dict, Union, Any

from typings.optional import Primitive
from typings.work_path import WorkPath


class LogFormat(Enum):
    [
        BINARY,
        JSON_LINE
    ] = [
        '.bin',
        '.jsonl'
    ]


Module = Dict[str, Union[Primitive, 'Module']]
Configuration = Dict[str, Union[Primitive, Module]]


class Output:
    slug = None

    def __init__(self, out_path: WorkPath, log_format: LogFormat):
        self._path = out_path
        self._format = log_format

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def config(self, filename: str) -> Any:
        raise NotImplementedError

    def __config__(self) -> Configuration:
        return {
            'slug': self.slug,
            'out_path': self._path,
            'log_format': self._format
        }


__all__ = [
    'Output',
    # types
    'LogFormat',
    'Configuration'
]
