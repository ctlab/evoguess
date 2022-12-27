from .single import Single
from .chunks import Chunks

shapings = {
    Single.slug: Single,
    Chunks.slug: Chunks,
}

__all__ = [
    'Single',
    'Chunks',
]
