class Solver:
    slug = 'solver'
    name = "Solver"

    def solve(self, clauses, assumptions, **kwargs):
        raise NotImplementedError

    def propagate(self, clauses, assumptions, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return self.name

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name
        }


__all__ = [
    'Solver'
]
