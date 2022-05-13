class Measure:
    key = None
    slug = 'measure'
    name = 'Measure'

    def __init__(self, *args, **kwargs):
        self.budget = kwargs.get('budget')

    def get(self, stats, status):
        # todo: check lower bound and change status!
        return stats.get(self.key, 0), status

    def limits(self):
        return {self.key: self.budget} if self.budget else {}

    def __str__(self):
        return self.name

    def __info__(self):
        return {
            'key': self.key,
            'slug': self.slug,
            'name': self.name,
            'budget': self.budget
        }


__all__ = [
    'Measure'
]
