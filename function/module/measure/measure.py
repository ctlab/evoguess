class Measure:
    key = None
    slug = 'measure'
    name = 'Measure'

    def __init__(self, *args, **kwargs):
        self.least = kwargs.get('least')
        self.budget = kwargs.get('budget')
        # status for over budget case
        self.over = kwargs.get('over', 'OVER')
        # status for under least case
        self.under = kwargs.get('under', 'UNDER')

    def check_and_get(self, stats, status):
        value = stats.get(self.key, 0)
        if self.least and value < self.least:
            status = self.over
        return value, status or self.under

    def limits(self):
        return {self.key: self.budget} if self.budget else {}

    def __str__(self):
        return self.name

    def __info__(self):
        return {
            'key': self.key,
            'slug': self.slug,
            'name': self.name,
            'over': self.over,
            'under': self.under,
            'least': self.least,
            'budget': self.budget,
        }


__all__ = [
    'Measure'
]
