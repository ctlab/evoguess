import os
import json
import time
import datetime

from util.error import *
from util.const import EXPERIMENT_PATH

[
    CREATED,
    OPENED,
    CLOSED
] = range(3)


def dt_name():
    today = datetime.datetime.today()
    z = lambda n: ('0%s' if n <= 9 else '%s') % n
    date = f'{today.year}.{z(today.month)}.{z(today.day)}'
    time = f'{z(today.hour)}:{z(today.minute)}:{z(today.second)}'
    return f'{date}_{time}'


class Output:
    slug = 'output'
    name = 'Output'

    def __init__(self, path, *args, **kwargs):
        self.name = None
        self.path = path
        self.scheme = None
        self.status = CREATED
        self.debug_verb = kwargs.get('debug_verb', 0)

    def open(self, scheme):
        if self.status != CREATED:
            raise AlreadyOpenedError()

        if not os.path.exists(EXPERIMENT_PATH):
            raise DirectoryNotExistsError(EXPERIMENT_PATH)

        self.path = os.path.join(EXPERIMENT_PATH, self.path)
        os.makedirs(self.path, exist_ok=True)

        name = f'{dt_name()}-?'
        path = os.path.join(self.path, name)
        while True:
            try:
                os.mkdir(path)
                break
            except FileExistsError:
                time.sleep(1)
                name = f'{dt_name()}-?'
                path = os.path.join(self.path, name)

        self.path, self.name = path, name
        self.status = OPENED
        self.scheme = scheme
        return self

    def close(self):
        if self.status != OPENED:
            raise AlreadyClosedError()

        name = self.name.replace('?', dt_name())
        path = self.path.replace(self.name, name)
        os.rename(self.path, path)

        self.path, self.name = path, name
        self.status = CLOSED
        return self

    def is_open(self):
        return self.status == OPENED

    def info(self, **kwargs):
        assert self.is_open(), 'Output isn\'t open'
        info_path = os.path.join(self.path, 'INFO')
        with open(info_path, 'w+') as file:
            file.write(json.dumps(kwargs, indent=2))
        return self

    def write(self, file, *strings: str):
        assert self.is_open(), 'Output isn\'t open'
        file_path = os.path.join(self.path, file)
        with open(file_path, 'a+') as f:
            f.writelines(['%s\n' % s for s in strings])
        return self

    def log(self, *objects):
        raise NotImplementedError

    def debug(self, verbosity: int, level: int, *strings: str):
        if self.debug_verb >= verbosity:
            prefix = f"{datetime.datetime.today()} --{'--' * level}"
            strings = [f'{prefix} {string}' for string in strings]
            return self.write('debug', *strings)
        return self

    def error(self, module, exception):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'path': self.path,
            'scheme': self.scheme,
            'debug_verb': self.debug_verb
        }


__all__ = [
    'Output'
]
