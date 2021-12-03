from .e0 import *
from .a5_1 import *

from .asg import *
from .grain import *
from .trivium import *

from .sorting import *

from .geffe import *
from .volfram import *

from .php import *
from .qap import *
from .sgen import *
from .domain import *
from .crafted import *
from .cruxmiter import *


def try_int(c):
    try:
        return int(c)
    except ValueError:
        return c


def get_instance(name):
    args = []
    if ':' in name:
        [name, args] = name.split(':')
        args = map(try_int, args.split('_'))
    return {
        'e0': E0,
        'a5': A5_1,
        'asg': ASG,
        'gr': Grain,
        # trivium
        'biv': Bivium,
        'tr': Trivium,
        'tr64': Trivium_64,
        'tr96': Trivium_96,
        # sorting
        'bvi': BubbleVsInsert,
        'bvp': BubbleVsPancake,
        'bvs': BubbleVsSelection,
        'pvs': PancakeVsSelection,
        # crafted
        'php': PHP,
        'qap': QAP,
        'sgen': SGEN,
        'domain': Domain,
        'mphp': MatrixPHP,
        'crafted': Crafted,
        'cruxmiter': Cruxmiter,
        # test
        'geffe': Geffe,
        'volfram': Volfram
    }[name](*args)


__all__ = ['get_instance']
