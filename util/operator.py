from functools import reduce


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return reduce(_getattr, [obj] + attr.split('.'))


def attreq(attr, value):
    return lambda obj: getattr(obj, attr) == value
