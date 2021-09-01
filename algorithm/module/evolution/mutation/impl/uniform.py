from ..mutation import *


class Uniform(Mutation):
    slug = 'mutation:uniform'
    name = 'Uniform(Mutation)'

    def __init__(self, scale=1., **kwargs):
        self.scale = scale
        super().__init__(**kwargs)

    def mutate(self, ind: Point) -> Point:
        v = ind.backdoor.get_mask()
        p = self.scale / len(v)
        distribution = self.roll_distribution(p, len(v))

        for j in range(len(v)):
            if p > distribution[j]:
                v[j] = not v[j]

        return Point(ind.backdoor.get_copy(v))

    def __info__(self):
        return {
            **super().__info__(),
            'scale': self.scale
        }


__all__ = [
    'Point',
    'Uniform'
]
