from ..instance import *

seeds = {
    28: 8,
    29: 4,
    32: 4
}


class Cruxmiter(Instance):
    base = 2
    tag = 'cruxmiter'

    def __init__(self, bits, seed=None):
        seed = seeds[bits] if seed is None else seed
        self.type = f"{bits}seed{seed}"
        self.name = f'Instance: Cruxmiter {bits} (seed: {seed})'
        self.cnf_path = self.build_cnf_path(self.tag, f"{self.tag}{self.type}")
        super().__init__(
            secret_key=SecretKey(1, bits)
        )


__all__ = [
    'Cruxmiter'
]
