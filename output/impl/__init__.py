from .vector_diff import VectorDiff
from .vector_full import VectorFull

outputs = {
    VectorFull.slug: VectorFull,
    VectorDiff.slug: VectorDiff
}

__all__ = [
    'outputs',
    # impls
    'VectorFull',
    'VectorDiff'
]
