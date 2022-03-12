from util.comparable import Comparable


class Point(Comparable):
    def __init__(self, comparator, backdoor):
        self.backdoor = backdoor
        super().__init__(comparator)

        self.estimation = None

    def set(self, **estimation):
        if not self.estimation:
            self.estimation = estimation
        else:
            raise Exception('Estimation already set')

    def value(self):
        return self.estimation.get('value', None)

    def __len__(self):
        return len(self.backdoor)


Vector = [Point]

__all__ = [
    'Point',
    'Vector',
]
