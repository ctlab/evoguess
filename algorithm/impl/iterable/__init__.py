from .plus_walker import PlusWalker
from .tabu_search import TabuSearch

algorithms = {
    PlusWalker.slug: PlusWalker,
    TabuSearch.slug: TabuSearch,
}

__all__ = [
    'TabuSearch',
]
