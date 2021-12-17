from util.operator import rgetattr

class Preprocess:
    slug = 'preprocess'
    name = 'Preprocess'

    def __init__(self, algorithm, *args, **kwargs):
        self.algorithm = algorithm

    def _get(self, attr):
        return rgetattr(self.algorithm, attr)

    def run(self):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }


__all__ = [
    'Preprocess'
]
