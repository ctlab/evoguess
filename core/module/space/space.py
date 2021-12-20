from instance import Instance


class Space:
    slug = 'space'
    name = 'Space'

    def __init__(self, initial):
        self.initial = initial

    def get_root(self, instance: Instance):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name
        }


__all__ = [
    'Space',
    'Instance'
]
