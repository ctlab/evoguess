from ..space import *

from instance.impl.instance import Instance
from instance.module.variables import Variables, Backdoor


class SearchSet(Space):
    slug = 'space:search_set'

    def __init__(self, variables: Variables, **kwargs):
        super().__init__(**kwargs)
        self.variables = variables

    # noinspection PyProtectedMember
    def get_backdoor(self, instance: Instance) -> Backdoor:
        return Backdoor(
            from_vars=self.variables._vars,
            from_file=self.variables.filepath,
        )

    def __info__(self):
        return {
            **super().__info__(),
            'variables': self.variables.__info__(),
        }


__all__ = [
    'SearchSet'
]
