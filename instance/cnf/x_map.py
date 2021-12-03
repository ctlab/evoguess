import pickle
from os.path import exists

x_maps = {}


class XMAP:
    def __init__(self, data):
        self.data = data

    def get_cnf_var(self, variable, value):
        return self.data['%d-%d' % (variable, value)]

    @staticmethod
    def parse(path, key=None):
        if key is not None and key in x_maps:
            return x_maps[key]

        with open(path, 'rb') as f:
            data = pickle.load(f)
            x_map = XMAP(data)

            if key is not None:
                x_maps[key] = x_map
            return x_map


if __name__ == "__main__":
    p, h = 20, 21
    path = './template/php/matrix/chr_%d_%d-x.pickle' % (p, h)
    if not exists(path):
        d = {}
        for i in range(p):
            for j in range(h):
                d['%d-%d' % (i, j)] = i * h + j + 1

        print('Writing...')
        with open(path, 'bw+') as f:
            pickle.dump(d, f)

    x_map = XMAP.parse(path)
    print(len(x_map.data), x_map.data)

__all__ = [
    'XMAP'
]
