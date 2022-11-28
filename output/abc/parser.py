import os
import json

from typing import Iterable, Any

from .output import Output, LogFormat, Configuration

from typings.work_path import WorkPath
from typings.error import OutputSessionError


class Parser(Output):
    _session = None

    def __init__(self, out_path: WorkPath, *log_dirs: str,
                 log_format: LogFormat = LogFormat.JSON_LINE):
        super().__init__(out_path, log_format)
        self.log_dirs = log_dirs

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def config(self, filename: str = 'config.json') -> Configuration:
        if self._session is None:
            raise OutputSessionError

        filepath = self._session.to_file(filename)
        with open(filepath, 'r') as handle:
            return json.load(handle, indent=2)

    def read(self, filename: str) -> Iterable[str]:
        if self._session is None:
            raise OutputSessionError

        filepath = self._session.to_file(filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as handle:
                for line in iter(handle.readline, ''):
                    yield line

    def parse(self, *args, **kwargs) -> Any:
        raise NotImplementedError


__all__ = [
    'Parser'
]
