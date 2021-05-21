from util.bitmask import apply_masks


def decimal_to_base(number, bases):
    values = []
    for base in bases[::-1]:
        number, value = divmod(number, base)
        values.insert(0, value)
    return values


def map_values(values, mappers):
    return [mappers[i][value] for i, value in enumerate(values)]


class Dimension:
    def __init__(self, backdoor, cache, offset=0):
        self._cache = cache
        self.backdoor = backdoor

        self.offset = offset
        self.function = None
        self.dimension = self._generate(offset)

    def __iter__(self):
        offset_dimension = self.dimension[self.offset:]
        for i, item in enumerate(offset_dimension):
            yield i, self.function(item)

    def _generate(self, offset):
        full_size = self.backdoor.task_count()
        if full_size > self._cache.state.max_size:
            masks = self.backdoor.get_masks()
            self.function = lambda x: apply_masks(x, masks)
            dimension = self._cache.state[self.backdoor].numbers()
        else:
            bases, mappers = self.backdoor.get_bases(), self.backdoor.get_mappers()
            self.function = lambda x: map_values(decimal_to_base(x, bases), mappers)
            dimension = self._cache.state[self.backdoor].permutation()[offset:]

        return dimension

    def get(self, position):
        return self.function(self.dimension[position])


__all__ = [
    'Dimension'
]
