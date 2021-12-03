from ..mutation import *


class Configurator(Mutation):
    name = 'Mutation: Configurator'

    def __init__(self, *options, **kwargs):
        self.options = options
        self.function = options[0]['f']
        super().__init__(**kwargs)

    def mutate(self, i: Individual) -> Individual:
        return self.function.mutate(i)

    def configure(self, state):
        for option in self.options:
            if option['?'](state):
                self.function = option['f']
                return self.function

        return self.function

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            *('  ' + str(option['f']) for option in self.options)
        ]))


__all__ = [
    'Configurator'
]
