from copy import copy


def concat(*lists):
    return sum(lists, [])


def slice_by_size(size, _list):
    return [_list[i:i + size] for i in range(0, len(_list), size)]


def slice_by_count(count, _list):
    size = len(_list) // count
    return slice_by_size(len(_list) // count, _list)


def list_of(example, dimension):
    if hasattr(dimension, '__len__'):
        return [copy(example) for _ in dimension]
    else:
        return [copy(example) for _ in range(int(dimension))]


def first_non_zero_position(_list, direction=True):
    pos, delta = (0, 1) if direction else (len(_list) - 1, -1)
    while 0 < pos < len(_list) and not _list[pos]:
        pos += delta
    return pos


def side_trim(_list, at_start=True):
    i = first_non_zero_position(_list) if at_start else 0
    j = first_non_zero_position(_list, direction=False)
    return _list[i:j + 1]


def to_bit_string(_list):
    return ''.join(['1' if e else '0' for e in _list])


def unzip(_list):
    max_len = max(map(len, _list), default=0)
    result = [[] for _ in range(max_len)]
    for i, element in enumerate(result):
        for _tuple in _list:
            try:
                element.append(_tuple[i])
            except IndexError:
                element.append(None)
    return result
