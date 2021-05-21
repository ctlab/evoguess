import json

from .._abc.output import *


class JSONOut(Output):
    slug = 'output:json'
    name = 'JSON Output'

    def log(self, *objects):
        self.write('log', *map(json.dumps, objects))

    def error(self, module, exception):
        self.write('log', json.dumps({
            'module': module,
            'exception': repr(exception)
        }))


__all__ = [
    'JSONOut'
]
