class Measure:
    key = None
    slug = 'measure'
    name = 'Measure'

    def get(self, stats):
        return max(1, stats.get(self.key, 0))

    def __info__(self):
        return {
            'key': self.key,
            'slug': self.slug,
            'name': self.name,
        }

    def __str__(self):
        return self.name


__all__ = [
    'Measure'
]
