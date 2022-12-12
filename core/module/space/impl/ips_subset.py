from typing import Dict, Any

from instance import Instance
from instance.module.variables import Backdoor

from ..space import Space


class IpsSubset(Space):
    def get_backdoor(self, instance: Instance) -> Backdoor:
        pass

    def __config__(self) -> Dict[str, Any]:
        pass


__all__ = [
    'IpsSubset'
]
