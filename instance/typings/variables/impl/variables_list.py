from ..variables import Variables


class VariablesList(Variables):
    slug = 'variables:list'
    name = 'VariablesList'

    def __init__(self, _list):
        super().__init__(_list)

    def __str__(self):
        return "%s" % self._list

    def __copy__(self):
        return VariablesList(self._list)

    def variables(self):
        return self._list

    def __info__(self):
        return {
            **super().__info__(),
            'list': self._list
        }


__all__ = [
    'VariablesList'
]
