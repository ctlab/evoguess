from .tabu_search import TabuSearch

algorithms = {
    TabuSearch.slug: TabuSearch,
}

__all__ = [
    'TabuSearch',
]
