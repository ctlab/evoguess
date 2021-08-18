from .._abc.output import *

import json
from uuid import uuid4

backdoor_cache = {}


class JSONOut(Output):
    slug = 'output:json'
    name = 'JSON Output'

    def make_replace(self, backdoors):
        replace, objects = {}, []
        for key in map(repr, backdoors):
            if key not in backdoor_cache:
                guid = uuid4().hex
                replace[key] = guid
                backdoor_cache[key] = guid
                objects.append({'guid': guid, 'backdoor': key})
            else:
                replace[key] = backdoor_cache[key]

        self.write('backdoors', *map(json.dumps, objects))
        return replace

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
