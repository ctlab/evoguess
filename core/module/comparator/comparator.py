class Comparator:
    slug = None

    def compare(self, object1, object2):
        raise NotImplementedError

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug,
        }


__all__ = [
    'Comparator'
]
