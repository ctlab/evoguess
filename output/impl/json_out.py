from .._abc.output import *

import json


class JSONOut(Output):
    slug = 'output:json'
    name = 'JSON Output'

    def log(self, *objects):
        self.write('log', *map(json.dumps, objects))

    def error(self, module, exception):
        self.write('errors', json.dumps({
            'module': module,
            'exception': repr(exception)
        }))


__all__ = [
    'JSONOut'
]
