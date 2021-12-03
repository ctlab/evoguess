import os
import tarfile
# import sqlite3
from time import sleep
from datetime import datetime
from os.path import join, abspath
from os import makedirs, mkdir, rename, remove
from typing import Iterable

CREATED = 'CREATED'
OPENED = 'OPENED'
CLOSED = 'CLOSED'


class NotOpenedError(Exception):
    """The Output hasn't open yet."""
    pass


class AlreadyOpenedError(Exception):
    """The Output already opened."""
    pass


class AlreadyClosedError(Exception):
    """The Output already closed."""
    pass


def dt_now(filename=False):
    if not filename:
        return str(datetime.today())

    today = datetime.today()
    z = lambda n: ('0%s' if n <= 9 else '%s') % n
    date = '%s.%s.%s' % (today.year, z(today.month), z(today.day))
    time = '%s:%s:%s' % (z(today.hour), z(today.minute), z(today.second))
    return '%s_%s' % (date, time)


class Output:
    name = 'Output'

    def __init__(self, path, **kwargs):
        self.path = path
        self.counter = -1
        self.kwargs = kwargs
        self.status = CREATED

        self._log_file = None
        self._debug_file = None
        self._extra_paths = []

        self._debug_verbosity = kwargs.get('dverb', 0)

    def _mkroot(self):
        try:
            name = '%s-?' % dt_now(True)
            path = join(self.path, name)
            mkdir(path)

            self.name = name
            self.path = path
            return True
        except FileExistsError:
            return False

    def open(self):
        if self.status != CREATED:
            raise AlreadyOpenedError()

        makedirs(self.path, exist_ok=True)
        while not self._mkroot():
            sleep(1)

        self.status = OPENED
        return self

    def close(self):
        if self.status != OPENED:
            raise AlreadyClosedError()

        arch_extra_paths = []
        for extra_path in self._extra_paths:
            try:
                target = join(self.path, extra_path)
                tar_path = join(self.path, '%s.tar.gz' % extra_path)
                with tarfile.open(tar_path, "w:gz") as tar:
                    tar.add(target, arcname=extra_path)

                arch_extra_paths.append(extra_path)
            except Exception as e:
                self.error('Output', 'Error in archiving process of %s' % extra_path, e)

        new_name = self.name.replace('?', dt_now(True))
        new_path = self.path.replace(self.name, new_name)
        rename(self.path, new_path)

        self.path = new_path
        self.name = new_name
        self.status = CLOSED

        self._create_script('clear', *[
            'rm -rf %s\n' %
            abspath(join(self.path, extra_path))
            for extra_path in arch_extra_paths
        ])
        return self

    def _create_script(self, name, *commands):
        script_path = join(self.path, '%s.sh' % name)
        with open(script_path, "w+") as f:
            f.writelines(['#!/bin/bash\n\n', *commands])
        os.system('chmod +x %s' % script_path)

    def register(self, extra_path):
        if self.status == CREATED:
            raise NotOpenedError()

        path = join(self.path, extra_path)
        makedirs(path, exist_ok=True)
        self._extra_paths.append(extra_path)
        return len(self._extra_paths) - 1

    def info(self, *strings: Iterable[str]):
        if self.status == CREATED:
            raise NotOpenedError()

        info_path = join(self.path, 'INFO')
        with open(info_path, 'w+') as f:
            f.writelines(list(strings))
        return self

    def is_open(self):
        if self.status == CREATED:
            raise NotOpenedError()
        if self.status == CLOSED:
            raise AlreadyClosedError()

    def touch(self):
        self.is_open()
        self.counter += 1

        lfile = self.kwargs.get('lfile', 'log')
        self._log_file = '%s_%d' % (lfile, self.counter)
        log_path = join(self.path, self._log_file)
        open(log_path, 'w+').close()

        dfile = self.kwargs.get('dfile', 'debug')
        self._debug_file = '%s_%d' % (dfile, self.counter)
        debug_path = join(self.path, self._debug_file)
        open(debug_path, 'w+').close()
        return self

    def log(self, *strings: Iterable[str]):
        return self.write(self._log_file, *strings)

    def debug(self, verbosity: int, level: int, *strings: Iterable[str]):
        if self._debug_verbosity >= verbosity:
            prefix = '%s --%s' % (dt_now(), '--' * level)
            strs = ['%s %s' % (prefix, s) for s in strings]
            return self.write(self._debug_file, *strs)
        return self

    def write(self, file, *strings: Iterable[str]):
        self.is_open()
        file_path = join(self.path, file)
        with open(file_path, 'a+') as f:
            f.writelines(['%s\n' % s for s in strings])
        return self

    def store(self, index, file, *strings):
        if self.status == CREATED:
            raise NotOpenedError()

        extra_path = self._extra_paths[index]
        store_path = join(self.path, extra_path, file)
        with open(store_path, 'a+') as f:
            f.writelines(list('%s\n' % s for s in strings))

    def get_db(self, name):
        if self.status == CREATED:
            raise NotOpenedError()

        db_path = join(self.path, '%s.db' % name)
        return None  # sqlite3.connect(db_path)

    def error(self, module, text, e):
        string = '%s: %s (%s)' % (module, text, repr(e))
        return self.write('ERRORS', string)


__all__ = [
    'Output'
]
