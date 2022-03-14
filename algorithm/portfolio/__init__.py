from .schema import schemas
from .portfolio import Portfolio

portfolio = {
    Portfolio.slug: Portfolio
}

__all__ = [
    'Portfolio'
]
