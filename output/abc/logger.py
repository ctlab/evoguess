import os
import json

from typing import Any
from datetime import datetime
from time import sleep, time as now

from .output import Output, LogFormat, Configuration

from typings.work_path import WorkPath
from typings.error import OutputSessionError


def date_now() -> str:
    return datetime.today().strftime("%Y.%m.%d-%H:%M:%S")


class Logger(Output):
    _name = None
    _session = None

    def __init__(self, out_path: WorkPath, log_format: LogFormat = LogFormat.JSON_LINE):
        super().__init__(out_path, log_format)
        self.session_enter = None

    def __enter__(self):
        session = None
        path = str(self._path)
        name = f'{date_now()}_?'
        while session is None:
            try:
                os.mkdir(os.path.join(path, name))
                session = self._path.to_path(name)
            except FileExistsError:
                name = sleep(1) or f'{date_now()}_?'

        self.session_enter = now()
        self._session = session
        self._name = name
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        path = self._session.base
        name = self._name.replace('?', date_now())
        os.rename(path, path.replace(self._name, name))
        self._session, self._name = None, None
        self.session_enter = None

    def config(self, config: Configuration, filename: str = 'config.json') -> 'Logger':
        if self._session is None:
            raise OutputSessionError

        filepath = self._session.to_file(filename)
        with open(filepath, 'w+') as handle:
            json.dump(config, handle, indent=2)
        return self

    def _write(self, *strings: str, filename: str) -> 'Logger':
        if self._session is None:
            raise OutputSessionError

        if len(strings) > 0:
            filepath = self._session.to_file(filename)
            with open(filepath, 'a+') as f:
                f.writelines([f'{s}\n' for s in strings])
        return self

    def write(self, *args: Any, **kwargs: Any) -> 'Logger':
        raise NotImplementedError

    # def debug(self, verbosity: int, level: int, *strings: str):
    #     if self.debug_verb >= verbosity:
    #         prefix = f"{datetime.datetime.today()} --{'--' * level}"
    #         strings = [f'{prefix} {string}' for string in strings]
    #         return self.write('debug', *strings)
    #     return self


__all__ = [
    'Logger'
]