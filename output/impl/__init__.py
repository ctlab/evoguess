from .vector_diff import VectorDiff
from .vector_logs import VectorLogs

outputs = {
    VectorLogs.slug: VectorLogs,
    VectorDiff.slug: VectorDiff
}

__all__ = [
    'outputs',
    # impls
    'VectorLogs',
    'VectorDiff'
]
