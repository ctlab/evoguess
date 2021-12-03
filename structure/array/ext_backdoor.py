from .backdoor import *


class ExtBackdoor(Backdoor):
    def find(self, var, insert=False):
        l, r = 0, self.length
        while r - l > 1:
            c = int((l + r) / 2)
            if self.list[c] > var:
                r = c
            else:
                l = c

        if insert:
            return l if self.list[l] >= var else r
        return l if self.list[l] == var else -1

    def add(self, var):
        pos = self.find(var, insert=True)

        if len(self.list) > pos and self.list[pos] == var:
            if not self.mask[pos]:
                self.mask[pos] = True
            else:
                raise Exception('Variable %d already exists in backdoor' % var)
        else:
            self.list.insert(pos, var)
            self.mask.insert(pos, True)

            self.length += 1
            self.max = self.list[-1]


__all__ = [
    'ExtBackdoor'
]
