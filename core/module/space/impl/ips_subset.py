from numpy import argsort
from typing import Dict, Any, Optional

from ..space import Space

from util.iterable import pick_by
from typings.optional import Str

from instance.impl import StreamCipher
from instance.module.encoding import Clause, CNFData
from instance.module.variables import Backdoor, Variables, Mask


def is2clause(clause: Clause, value: int) -> bool:
    index, size = 0, len(clause)
    while size > 2 and index < len(clause):
        index, literal = index + 1, clause[index]
        if literal == value:
            return False
        if value is not None:
            size -= 1

    return size <= 2


class IpsSubset(Space):
    slug = 'space:ips_subset'
    _subset = None

    def __init__(self, of_size: int, variables: Variables,
                 by_string: Str = None, by_mask: Optional[Mask] = None):
        super().__init__(by_string, by_mask)
        self.variables = variables
        self.of_size = of_size

    def get_backdoor(self, instance: StreamCipher) -> Backdoor:
        if not self._subset:
            data = instance.encoding.get_data()
            if isinstance(data, CNFData):
                variable_weights = []
                for var in self.variables:
                    counter_0 = 0
                    for value in var.supplements({var: 0})[0]:
                        for clause in data.clauses():
                            counter_0 += is2clause(clause, value)
                    counter_1 = 0
                    for value in var.supplements({var: 0})[0]:
                        for clause in data.clauses():
                            counter_1 += is2clause(clause, value)
                    variable_weights.append(counter_0 * counter_1)

                indexes = argsort(variable_weights)[::-1][:self.of_size]
                self._subset = pick_by(self.variables.variables(), indexes)

        return Backdoor(from_vars=self._subset)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'of_size': self.of_size,
            'by_mask': self.by_mask,
            'by_string': self.by_string,
            'variables': self.variables.__config__(),
        }


__all__ = [
    'IpsSubset'
]
