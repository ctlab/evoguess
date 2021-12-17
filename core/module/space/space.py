from instance import Instance


class Space:
    slug = 'space'
    name = 'Space'

    def __init__(self, initial):
        self.initial = initial

    def get(self, instance: Instance) -> [int]:
        raise NotImplementedError


__all__ = [
    'Space',
    'Instance'
]
