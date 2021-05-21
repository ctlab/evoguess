def to_bit(condition):
    return 1 if condition else 0


def in_mask(value, mask):
    return mask & (2 ** value)


def apply_mask(value, mask):
    return in_mask(value, mask) and value


def in_masks(values, masks):
    return list(map(in_mask, values, masks))


def apply_masks(values, masks):
    return list(map(apply_mask, values, masks))


def in_bits(value, bits):
    return bits[-value - 1]
