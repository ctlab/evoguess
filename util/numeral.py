from math import ceil, log2


def base_to_binary(base, *values):
    size = ceil(log2(base))
    return [base_to_binary2(size, value) for value in values]


def base_to_binary2(size, value):
    return [1 if value & (1 << (size - 1 - i)) else 0 for i in range(size)]


def binary_to_base(base, bits):
    size = ceil(log2(base))
    binaries = [bits[i * size:(i + 1) * size] for i in range(len(bits) // size)]
    return [binary_to_base2(size, binary) for binary in binaries]


def binary_to_base2(size, bits):
    return sum([1 << (size - 1 - i) for i, bit in enumerate(bits) if bit])


if __name__ == "__main__":
    for j in range(2, 100):
        old_values = list(range(j))
        bbits = sum(base_to_binary(j, *old_values), [])
        new_values = list(binary_to_base(j, bbits))
        assert len(old_values) == len(new_values)
        for (a, b) in zip(old_values, new_values):
            assert a == b, (a, b)

    print(binary_to_base2(12, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]))
    print(base_to_binary2(12, 2730))
