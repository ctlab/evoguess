class Cache:
    def __getattr__(self, key):
        return self.__dict__.get(key)

    def __setattr__(self, key, value):
        self.__dict__[key] = value


CACHE = Cache()

__all__ = [
    'CACHE'
]
