class Solver:
    name = "Solver"

    def solve(self, clauses, assumptions, **kwargs):
        raise NotImplementedError

    def str(self):
        return self.name


__all__ = [
    'Solver'
]
