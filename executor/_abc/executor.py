from os import cpu_count


class Executor:
    slug = 'executor'
    name = 'Executor'
    awaiter_dict = {}

    def __init__(self, *args, **kwargs):
        self.workers = kwargs.get('workers', cpu_count())
        # todo: add executor.free()

    def submit(self, fn, *args, **kwargs):
        raise NotImplementedError

    def submit_all(self, fn, tasks, payload):
        # todo: rewrite this method
        index_futures = []
        # for shape in self.shaping.get(self.workers, tasks):
        #     index = [task.index for task in shape]
        #     future = self.submit(fn, payload, shape)
        #     index_futures.append((index, future))
        return index_futures

    def get_awaiter(self, key='as_completed'):
        return self.awaiter_dict.get(key)

    def shutdown(self, wait=True):
        raise NotImplementedError

    def __str__(self):
        return self.name

    def __len__(self):
        return self.workers

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'workers': self.workers,
        }


__all__ = [
    'Executor'
]
