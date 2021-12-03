import json
import tarfile
from time import time as now
from os.path import join, sep


class UUIDCache:
    def __init__(self, path, name):
        self.archive, self.members = None, {}
        self.tar_path = join(path, '%s.tar.gz' % name)

        self.files = {}
        self.list = {}
        list_path = join(path, '%s.list' % name)
        with open(list_path, 'r') as f:
            for line in f.readlines():
                info = json.loads(line)
                self.list[info["key"]] = info

        print('Init UUID cache with %d backdoors' % len(self.list))

    def _lazy_load(self):
        if self.archive is not None:
            return

        timestamp = now()
        print('Start lazy loading archive')
        self.archive = tarfile.open(self.tar_path, 'r:gz')
        for member in self.archive.getmembers():
            uuid = member.name.split(sep)[-1]
            self.members[uuid] = member
        print('Archive was lazy loaded in %.2f seconds\n' % (now() - timestamp))

    def load(self, key):
        info = self.list.get(key)
        if info is None: return None

        uuid = info['uuid']
        if uuid in self.files:
            return self.files[uuid]

        self._lazy_load()
        member = self.members.get(uuid)
        if member is None: return None

        file = self.archive.extractfile(member)
        if file is None: return None

        content = file.read().decode('utf-8')
        json_file = json.loads(content)
        self.files[uuid] = json_file
        return json_file


__all__ = [
    'UUIDCache'
]
