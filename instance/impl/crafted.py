from ..instance import *

name_st = {
    'mod2c-3cage-unsat-10-2': 140,
    'mod2c-3cage-unsat-10-3': 140,
    'sgen1-unsat-85-100': 85,
    'sgen1-unsat-97-100': 97,
    'sgen1-unsat-103-100': 105,
    'sgen1-unsat-109-100': 109,
    'sgen1-unsat-115-100': 117,
    'gt-ordering-unsat-gt-035': 1225,
    'gt-ordering-unsat-gt-045': 2025,
    #
    'pmg-11-UNSAT': 169,
    'pmg-12-UNSAT': 190,
    'pmg-13-UNSAT': 409,
    'pmg-14-UNSAT': 577,
    'unsat-set-a-clqcolor-10-06-07': 175,
    'unsat-set-a-fclqcolor-10-06-07': 175,
}


class Crafted(Instance):
    base = 2
    tag = 'crafted'

    def __init__(self, name):
        self.type = name
        self.name = f'Instance: Crafted (name: {name})'
        self.cnf_path = self.build_cnf_path(self.tag, name)
        super().__init__(
            secret_key=SecretKey(1, name_st[name])
        )


__all__ = [
    'Crafted'
]
