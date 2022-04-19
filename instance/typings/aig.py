import os
import threading

from util.const import TEMPLATE_PATH

aig_source = {}
lock = threading.Lock()


class AIG:
    slug = 'aig'
    name = 'AIG'
    has_atmosts = False

    def __init__(self, path):
        self._path = path
        self.path = os.path.join(TEMPLATE_PATH, path)

    def _parse_aig(self):
        if self.path in aig_source:
            return

        print(f'read aig... ({self.path})')
        with open(self.path) as handle:
            aig_source[self.path] = handle.read()

    def source(self, assumptions=()):
        with lock:
            self._parse_aig()
            return ''.join([
                f'{aig_source[self.path]}\n',
                *(f'{2 * abs(x) + (x < 0)}\n' for x in assumptions)
            ])

    def __copy__(self):
        return AIG(self._path)

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'path': self._path,
        }
