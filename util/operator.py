def is_none(x):
    return x is None


def is_not_none(x):
    return x is not None


def smin(*args, key=None):
    return min(filter(is_not_none, args), key=key)


def smax(*args, key=None):
    return max(filter(is_not_none, args), key=key)


def sget(obj, key, default=None):
    try:
        return obj[key]
    except (KeyError, IndexError):
        return default


def scall(fn, *args, **kwargs):
    if any(map(is_none, args)) or any(map(is_none, kwargs.values())):
        return None
    return fn(*args, **kwargs)


def attreq(attr, value):
    return lambda obj: getattr(obj, attr) == value
