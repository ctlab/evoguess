class Shaping:
    slug = 'shaping'
    name = 'Shaping'

    def __init__(self):
        pass

    def get(self, size, tasks, seed=None):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name
        }
