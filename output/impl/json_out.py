from ..abc.output import *

import json
from uuid import uuid4

backdoor_cache = {}


class JSONOut(Output):
    slug = 'output:json'

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


__all__ = [
    'JSONOut'
]
