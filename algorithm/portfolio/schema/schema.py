from algorithm.typings import Vector, Point


class Schema:
    slug = 'schema'
    name = 'Schema'
    max_points = None
    min_select_size = None

    def get_points(self, vector: Vector, count: int) -> Vector:
        raise NotImplementedError

    def update_vector(self, vector: Vector, *points: Point) -> Vector:
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }

__all__ = [
    'Point',
    'Vector',
    'Schema',
]
