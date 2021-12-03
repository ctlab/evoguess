import json
from uuid import uuid4
from collections import namedtuple
from structure.array import Backdoor, DomainBackdoor


class UnsupportedTypeError(Exception):
    """The type is unsupported."""
    pass


class BackdoorCache:
    def __init__(self, output):
        self._best = None
        self._cache = {}
        self._output = output

        self.index = output.register('backdoors')

    def __contains__(self, backdoor):
        if not isinstance(backdoor, DomainBackdoor) and \
                not isinstance(backdoor, Backdoor):
            raise UnsupportedTypeError()

        key = str(backdoor)
        return key in self._cache

    def __getitem__(self, backdoor):
        if not isinstance(backdoor, DomainBackdoor) and \
                not isinstance(backdoor, Backdoor):
            raise UnsupportedTypeError()

        key = str(backdoor)
        return self._cache[key][1]

    def __setitem__(self, backdoor, payload):
        if not isinstance(backdoor, DomainBackdoor) and \
                not isinstance(backdoor, Backdoor):
            raise UnsupportedTypeError()

        key = str(backdoor)
        self._cache[key] = backdoor, payload

    def get(self, backdoor, default=None):
        if self.__contains__(backdoor):
            return self.__getitem__(backdoor)
        return default

    def dumps(self, backdoor: Backdoor):
        if not isinstance(backdoor, DomainBackdoor) and \
                not isinstance(backdoor, Backdoor):
            raise UnsupportedTypeError()

        info = {
            'uuid': uuid4().hex,
            'key': str(backdoor),
        }
        _, payload = self._cache[info['key']]
        info['count'] = len(payload[0])

        string = json.dumps({
            'backdoor': str(backdoor),
            'count': len(payload[0]),
            'time': payload[1]['time'],
            'value': payload[1]['value'],
            'job_time': payload[1]['job_time'],
            'process_time': payload[1]['process_time'],
            'cases': payload[0],
        }, indent=2)
        self._output.store(self.index, info['uuid'], string)
        self._output.write('backdoors.list', json.dumps(info))

        # if self._best[1]
