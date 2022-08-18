from typing import Dict, Tuple

from typings.optional import Float


class Measure:
    key = None
    slug = 'measure'

    def __init__(self, budget: Float, at_least: Float, **kwargs):
        self.budget = budget
        self.at_least = at_least
        # status for over budget case
        self.over = kwargs.get('over', 'OVER')
        # status for under least case
        self.under = kwargs.get('under', 'UNDER')

    def check_and_get(self, stats, status) -> Tuple[Float, str]:
        value = stats.get(self.key, 0)
        if self.at_least and value < self.at_least:
            status = self.over
        return value, status or self.under

    def limits(self) -> Dict[str, Float]:
        return {self.key: self.budget} if self.budget else {}

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
    'Measure'
]
