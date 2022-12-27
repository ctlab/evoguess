class Shaping:
    slug = 'shaping'
    name = 'Shaping'

    def __init__(self, *args, **kwargs):
        pass

    def get(self, size, tasks):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name
        }
