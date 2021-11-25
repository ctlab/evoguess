def is_none(x):
    return x is None


def is_not_none(x):
    return x is not None


def smin(*args, key=None):
    return min(filter(is_not_none, args))  # , key=key)


def smax(*args, key=None):
    return max(filter(is_not_none, args))  # , key=key)


def sget(obj, key, default=None):
    try:
        return obj[key]
    except (KeyError, IndexError):
        return default


def scall(fn, default=None, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except:
        return default


def attreq(attr, value):
    return lambda obj: getattr(obj, attr) == value
