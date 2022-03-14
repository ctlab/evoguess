from .._abc import AlgorithmABC

from ..typings import Vector
from util.array import concat
from util.operator import smin
from util.collection import for_each


class Portfolio(AlgorithmABC):
    awaited_count = None
    slug = 'algorithm:portfolio'
    name = 'Algorithm: Portfolio'

    def __init__(self, schemas, *args, **kwargs):
        self.schemas = schemas
        super().__init__(*args, **kwargs)
        self.sync_delay = kwargs.get('sync_delay', 10)
        self.awaited_count = kwargs.get('awaited_count', 1)

    def process(self, estimated: Vector) -> Vector:
        vectors = {i: estimated for i in range(len(self.schemas))}
        p_handles = {i: [] for i in range(len(self.schemas))}

        sync_counter = self.sync_delay
        while not self.limit.exhausted():
            index = self.limit.increase('index')
            for i, schema in enumerate(self.schemas):
                if schema.max_points > len(p_handles[i]):
                    count = schema.max_points - len(p_handles[i])
                    points = schema.get_points(vectors[i], count)
                    p_handles[i].extend(map(self._queue, points))

            all_p_handles = concat(*p_handles.values())
            all_estimated, _ = self._await(*all_p_handles, count=self.awaited_count)
            for i, schema in enumerate(self.schemas):
                estimated, next_p_handles = [], []
                for point, handle in p_handles[i]:
                    if point in all_estimated:
                        estimated.append(point)
                    else:
                        next_p_handles.append((point, handle))

                p_handles[i] = next_p_handles
                vectors[i] = schema.update_vector(vectors[i], *estimated)

            sync_counter -= 1
            if sync_counter <= 0:
                sync_counter, sync_point = self.sync_delay, None
                for i, schema in enumerate(self.schemas):
                    point = sorted(vectors[i])[0]
                    sync_point = smin(sync_point, point)
                for i, schema in enumerate(self.schemas):
                    if sync_point not in vectors[i]:
                        vectors[i] = [sync_point, *vectors[i]][:-1]
            self._proceed_index_results(index, vectors)
        for_each(concat(*p_handles.values()), self._cancel)

        return [sorted(vs)[0] for vs in vectors.values()]

    def _proceed_index_results(self, index: int, vectors):
        backdoors = []
        for i, vector in vectors.items():
            backdoors.extend([p.backdoor for p in vector])
        replace = self.output.make_replace(backdoors)
        self.output.log({
            'index': index,
            'spent': round(self.limit.get('time'), 2),
            'schemas': {
                i: [point.to_dict(replace) for point in vectors[i]]
                for i, schema in enumerate(self.schemas)
            }
        })


__all__ = [
    'Portfolio'
]
