from .tabu_search import TabuSearch
from .mu_plus_lambda import MuPlusLambda
from .mu_comma_lambda import MuCommaLambda

algorithms = {
    TabuSearch.slug: TabuSearch,
    MuPlusLambda.slug: MuPlusLambda,
    MuCommaLambda.slug: MuCommaLambda
}

__all__ = [
    'TabuSearch',
    'MuPlusLambda',
    'MuCommaLambda'
]
