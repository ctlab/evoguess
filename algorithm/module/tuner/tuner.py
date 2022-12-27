class Tuner:
    slug = None
    name = 'Tuner'

    def tune(self, limit, *args, **kwargs):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }


__all__ = [
    'Tuner'
]
