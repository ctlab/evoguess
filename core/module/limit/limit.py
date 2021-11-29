class Limit:
    key = None
    slug = None
    name = 'Limit'

    def __init__(self, value):
        self.limits = {
            'time': 0,
            'restarts': 0,
            'iteration': 0,
            'stagnation': 0
        }
        self.limit = value

    def increase(self, key, value=1):
        self.limits[key] += value
        return self.limits[key]

    def set(self, key, value):
        self.limits[key] = value
        return value

    def get(self, key, default=0):
        return self.limits.get(key, default)

    def exhausted(self) -> bool:
        return self.get(self.key) > self.limit

    def left(self) -> dict:
        return {self.key: max(0, self.limit - self.get(self.key))}

    def __info__(self):
        return {
            'key': self.key,
            'slug': self.slug,
            'name': self.name,
            'limit': self.limit
        }

    def __str__(self):
        return self.name


__all__ = [
    'Limit'
]
