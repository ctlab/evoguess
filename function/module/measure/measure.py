from typing import Tuple
from typings.optional import Float, Str

Budget = Tuple[Str, Float]
EMPTY_BUDGET = ('', None)

STATUSES = {
    True: 'SAT',
    None: 'UNDET',
    False: 'UNSAT'
}


class Measure:
    key = None
    slug = 'measure'

    def __init__(self,
                 budget: Float = None,
                 at_least: Float = None,
                 over_status: Str = 'OVER',
                 under_status: Str = 'UNDER'):
        self.budget = budget
        self.at_least = at_least
        self.over_status = over_status
        self.under_status = under_status

    def get_budget(self) -> Budget:
        return self.key, self.budget

    def check_and_get(self, stats, status) -> Tuple[Float, str]:
        value = stats.get(self.key)
        if self.budget and status is None:
            return value, self.over_status
        if self.at_least and value < self.at_least:
            return value, self.under_status
        return value, STATUSES[status]

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'key': self.key,
            'slug': self.slug,
            'over': self.over,
            'under': self.under,
            'budget': self.budget,
            'at_least': self.at_least,
        }


__all__ = [
    'Budget',
    'Measure',
    # const
    'EMPTY_BUDGET'
]
