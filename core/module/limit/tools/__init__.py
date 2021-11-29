from .any import *
from ..impl import limits as modules

from util import load_modules

limits = {
    Any.slug: lambda kwargs: Any(**load_modules(modules, **kwargs))
}
