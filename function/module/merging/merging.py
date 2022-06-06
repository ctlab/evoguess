class Merging:
    key = None
    slug = 'merging'
    name = 'Merging'

    def __init__(self, rules):
        self.rules = rules

    def __str__(self):
        return self.name

    def __info__(self):
        return {
            'key': self.key,
            'slug': self.slug,
            'name': self.name,
        }


__all__ = [
    'Merging'
]
