class Solver:
    slug = 'solver'
    name = "Solver"

    def solve(self, instance, assumptions, **kwargs):
        raise NotImplementedError

    def propagate(self, instance, assumptions, **kwargs):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name
        }

    def str(self):
        return self.name


__all__ = [
    'Solver'
]
