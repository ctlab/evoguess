class Limit:
    name = 'Limit'

    def __init__(self):
        self.limits = {
            'time': 0,
            'restarts': 0,
            'iteration': 0,
            'predictions': 0,
        }

    def increase(self, key, value=1):
        self.limits[key] += value
        return self.limits[key]

    def set(self, key, value):
        self.limits[key] = value
        return value

    def get(self, key, default=0):
        return self.limits.get(key, default)

    def exhausted(self) -> bool:
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Limit'
]
