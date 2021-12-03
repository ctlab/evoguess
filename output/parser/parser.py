from typing import List, Tuple

from os import listdir
from os.path import join

from structure.individual import Individual
from output.parser.uuid_cache import UUIDCache

Iteration = List[Individual]


class Parser:
    def parse(self, path: str) -> List[Iteration]:
        files = listdir(path)
        log_files = [file for file in files if 'log' in file]
        print('Found %d log file(s)' % len(log_files))

        iterations = []
        cache = UUIDCache(path, 'backdoors')
        for log_file in sorted(log_files):
            log_path = join(path, log_file)
            data = self._read(log_path)
            iterations.extend(self.parse_data(data, cache))
        return iterations

    def parse_data(self, data: str, cache: UUIDCache) -> List[Iteration]:
        raise NotImplementedError

    @staticmethod
    def _read(path: str) -> list[str]:
        with open(path) as f:
            return [x[:-1] for x in f.readlines()]


__all__ = [
    'Parser',
    'Iteration'
]
