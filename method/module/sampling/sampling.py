class Sampling:
    slug = 'sampling'
    name = 'Sampling'

    def get_count(self, backdoor, values=()):
        raise NotImplementedError

    def get_size(self):
        raise NotImplementedError

    def report(self, values):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }

    def __str__(self):
        return self.name


__all__ = [
    'Sampling'
]
