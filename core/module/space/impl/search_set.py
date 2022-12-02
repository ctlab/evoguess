from ..space import Space

from typings.optional import Str
from instance.impl.instance import Instance
from instance.module.variables import Mask, Variables, Backdoor


class SearchSet(Space):
    slug = 'space:search_set'

    def __init__(self, variables: Variables, by_mask: Mask = None, by_string: Str = None):
        super().__init__(by_mask, by_string)
        self.variables = variables

    # noinspection PyProtectedMember
    def get_backdoor(self, instance: Instance) -> Backdoor:
        return Backdoor(
            from_vars=self.variables._vars,
            from_file=self.variables.filepath,
        )

    def __config__(self):
        return {
            'slug': self.slug,
            'by_mask': self.by_mask,
            'by_string': self.by_string,
            'variables': self.variables.__config__(),
        }


__all__ = [
    'SearchSet'
]
