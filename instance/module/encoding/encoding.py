from typing import Any
from os.path import join

from util.const import TEMPLATE_PATH
from util.lazy_file import get_file_data


class Encoding:
    slug = 'encoding'

    def __init__(self, from_file: str = None):
        self.filepath = from_file

    def get_data(self) -> Any:
        raise NotImplementedError

    def get_raw_data(self) -> str:
        # todo: remove env PATHS
        return get_file_data(join(TEMPLATE_PATH, self.filepath))

    def __info__(self):
        return {
            'slug': self.slug,
            'from_file': self.filepath,
        }


__all__ = [
    'Any',
    'Encoding'
]
