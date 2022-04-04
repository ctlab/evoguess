from util.comparable import Comparable


class Point(Comparable):
    def __init__(self, comparator, backdoor):
        self.estimation = None
        self.backdoor = backdoor
        super().__init__(comparator)

    def __len__(self):
        return len(self.backdoor)

    def set(self, **estimation) -> 'Point':
        if not self.estimation:
            self.estimation = estimation
            return self
        else:
            raise Exception('Estimation already set')

    def value(self) -> float:
        return self.estimation.get('value', None)


Vector = [Point]

__all__ = [
    'Point',
    'Vector',
]
