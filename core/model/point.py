from typings.ordered import Ordered


class Point(Ordered):
    def __init__(self, comparator, backdoor):
        self.estimation = None
        self.backdoor = backdoor
        super().__init__(comparator)

    def __len__(self):
        return len(self.backdoor)

    def set(self, **estimation) -> 'Point':
        if self.estimation is None:
            self.estimation = estimation
            return self
        else:
            raise Exception('Estimation already set')

    def estimated(self) -> bool:
        return self.estimation is not None

    def value(self) -> float:
        return self.estimation.get('value', None)


Vector = [Point]

__all__ = [
    'Point',
    'Vector',
]
