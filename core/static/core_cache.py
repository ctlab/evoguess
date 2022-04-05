class CoreCache:
    def __getattr__(self, key):
        return self.__dict__.get(key)

    def __setattr__(self, key, value):
        self.__dict__[key] = value


CORE_CACHE = CoreCache()

__all__ = [
    'CORE_CACHE'
]
