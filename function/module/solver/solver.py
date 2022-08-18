class Solver:
    slug = 'solver'

    def solve(self, clauses, assumptions, **kwargs):
        raise NotImplementedError

    def propagate(self, clauses, assumptions, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug
        }


__all__ = [
    'Solver'
]
