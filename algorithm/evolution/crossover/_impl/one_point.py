from ..crossover import *


class OnePoint(Crossover):
    name = 'Crossover: One-point'

    def cross(self, i1: Individual, i2: Individual) -> Tuple[Individual, Individual]:
        vbd, wbd = i1.backdoor, i2.backdoor
        v, w = vbd.get_mask(), wbd.get_mask()

        direction = self.random_state.rand()
        pos = self.random_state.randint(len(v))
        a, b = (0, pos) if direction < 0.5 else (pos, len(v))

        for i in range(a, b):
            v[i], w[i] = w[i], v[i]

        return Individual(vbd.get_copy(v)), Individual(wbd.get_copy(w))


__all__ = [
    'OnePoint'
]
