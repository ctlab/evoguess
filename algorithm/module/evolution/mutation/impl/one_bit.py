from ..mutation import *


class OneBit(Mutation):
    slug = 'mutation:one-bit'
    name = 'One Bit(Mutation)'

    def mutate(self, ind: Point) -> Point:
        mask = ind.backdoor.get_mask()
        i = self.random_state.randint(0, len(mask))

        mask[i] = not mask[i]
        return Point(ind.backdoor.get_copy(mask))


__all__ = [
    'OneBit'
]
