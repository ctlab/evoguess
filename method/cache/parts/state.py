from collections import namedtuple

from numpy.random import RandomState

BackdoorState = namedtuple('BackdoorState', ['numbers', 'permutation', 'get_function_seed'])


class State:
    def __init__(self, seed, max_size, step_size):
        self.seed = seed
        self.max_size = max_size
        self.step_size = step_size

        self.states = {}
        self.random_state = RandomState(seed=seed)

    def __getitem__(self, item):
        item_key = str(item)
        if item_key not in self.states:
            state = self.states[item_key] = {
                'list_seed': self.random_state.randint(0, 2 ** 31 - 1),
                'function_seed': self.random_state.randint(0, 2 ** 31 - 1),
                'base': item.base, 'size': len(item), 'power': item.task_count(),
            }
        else:
            state = self.states.get(item_key)

        return BackdoorState(
            lambda: self._numbers(state),
            lambda: self._permutation(state),
            lambda: state['function_seed'],
        )

    def _numbers(self, state):
        rs = RandomState(seed=state['list_seed'])
        shape = (self.max_size, state['size'])
        return rs.randint(1, state['base'] + 1, size=shape)
        #
        # if 'numbers' not in state:
        #     rs = RandomState(seed=state['list_seed'])
        #     shape = (self.max_size, state['size'])
        #     state['numbers'] = rs.randint(1, state['base'] + 1, size=shape)
        # return state['numbers'][offset:offset + count]

    def _permutation(self, state):
        rs = RandomState(seed=state['list_seed'])
        return rs.permutation(state['power'])

        # if 'permutation' not in state:
        #     rs = RandomState(seed=state['list_seed'])
        #     state['permutation'] = rs.permutation(state['power'])
        # return state['permutation'][offset:offset + count]


__all__ = [
    'State'
]
