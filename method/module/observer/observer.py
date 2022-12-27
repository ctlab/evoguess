class Observer:
    slug = 'observer'
    name = 'Observer'

    def __init__(self):
        pass

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }


__all__ = [
    'Observer'
]
