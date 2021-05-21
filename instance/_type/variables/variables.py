from numpy.random.mtrand import RandomState


def get_values(variables, seed=None, solution=None):
    if solution is not None:
        try:
            return [solution[x - 1] for x in variables]
        except IndexError:
            raise Exception('Solution have too few variables: %d' % len(solution))
    else:
        values = RandomState(seed=seed).randint(2, size=len(variables))
        return [x if values[i] else -x for i, x in enumerate(variables)]


class Variables:
    slug = 'variables'
    name = 'Variables'

    def __init__(self, _list):
        self.list = _list
        self.length = len(self.list)

    def snapshot(self):
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError

    def __len__(self):
        return len(self.snapshot())

    def __str__(self):
        variables, strings, i, j = self.snapshot(), [], 0, 1
        while i < len(variables):
            if j == len(variables) or variables[j] - variables[i] != j - i:
                if j - i > 2:
                    strings.append(f'{variables[i]}..{variables[j - 1]}')
                else:
                    strings.extend(f'{variables[k]}' for k in range(i, j))
                i, j = j, j + 1
            else:
                j += 1

        return f"[{' '.join(strings)}]({len(variables)})"

    def __iter__(self):
        return self.snapshot().__iter__()

    def __hash__(self):
        return hash(tuple(self.snapshot()))

    def __contains__(self, item):
        return item in self.snapshot()

    def values(self, **kwargs):
        return get_values(self.snapshot(), **kwargs)

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }


__all__ = [
    'Variables'
]
