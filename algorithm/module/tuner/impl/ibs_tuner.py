from ..tuner import *


class IBSTuner(Tuner):
    slug = 'tuner:ibs'
    name = 'IBS Tuner'

    def __init__(self, levels, limit_key, **kwargs):
        self.index = -1
        self.level = None
        self.levels = levels

        self.last_limit = 0
        self.limit_key = limit_key
        self.save_mode = kwargs.get('save_mode', True)
        self.value_bound = 0 if self.save_mode else float('inf')
        self.reset_after_increase = kwargs.get('reset_after_increase', False)

    def tune(self, limit, *args, **kwargs):
        if self.index + 1 >= len(self.levels):
            return

        limit_value = limit.get(self.limit_key)
        next_level = self.levels[self.index + 1]
        function = kwargs.get('method').function
        if self.save_mode:
            if limit_value <= self.last_limit:
                self.value_bound = 2 * next_level['value']
        self.last_limit = limit_value

        print('stagnation count:', limit_value, 'of', next_level['bound'])
        if limit_value >= next_level['bound']:
            value = next_level['value']
            if value < self.value_bound:
                self.index += 1
                self.level = next_level
                function.limit_value = value
                kwargs.get('output').debug(1, 1, f'Set budget to {value}')
                if self.reset_after_increase:
                    limit.set(self.limit_key, 0)

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'save_mode': self.save_mode,
            'reset_after_increase': self.reset_after_increase
        }


__all__ = [
    'IBSTuner'
]
