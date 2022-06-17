def xor(*args):
    return sum(args) % 2 == 1


def bent_4(x1, x2, x3, x4):
    return xor(x1 and x3, x2 and x4)


def majority(*args):
    return sum(args) > len(args) // 2


__all__ = [
    'xor',
    'bent_4',
    'majority'
]
