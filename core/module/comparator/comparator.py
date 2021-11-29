class Comparator:
    slug = None
    name = 'Comparator'

    def compare(self, object1, object2):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }


__all__ = [
    'Comparator'
]
