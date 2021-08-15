class Sampling:
    slug = 'sampling'
    name = 'Sampling'

    RANDOM = 'random'
    DIRECT = 'direct'
    REVERSED = 'reversed'

    def __init__(self, max_size, step_size, order=RANDOM):
        self.order = order
        self.max_size = max_size
        self.step_size = step_size

    def get_count(self, backdoor, values=()):
        raise NotImplementedError

    def report(self, values):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'order': self.order
        }

    def __str__(self):
        return self.name


__all__ = [
    'Sampling'
]
