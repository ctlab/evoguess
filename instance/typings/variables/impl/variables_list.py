from ..variables import Variables


class VariablesList(Variables):
    slug = 'VariablesList'
    name = 'VariablesList'

    def __init__(self, _list):
        super().__init__(_list)

    def __str__(self):
        return "%s" % _list

    def __copy__(self):
        return Interval(self.start, self.length)

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
