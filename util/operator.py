def attreq(attr, value):
    return lambda obj: getattr(obj, attr) == value
