from typing import Iterable, Tuple, Any, Callable, Optional

from numpy.random.mtrand import RandomState

Task = Iterable[Any]
Result = Iterable[Any]
Info = Tuple[float, Iterable[int]]


class Concurrency:
    name = "Concurrency"

    def __init__(self,
                 output,
                 random_seed: int,
                 *args, **kwargs
                 ):
        self.output = output
        self.random_seed = random_seed
        self.random_state = RandomState(seed=random_seed)

    def submit(self, f: Callable, *tasks: Task, **kwargs) -> Optional[int]:
        raise NotImplementedError

    def cancel(self, job_id: int) -> Optional[bool]:
        raise NotImplementedError

    def wait(self, job_ids, timeout: float) -> Info:
        raise NotImplementedError

    def get(self, job_id: int) -> Result:
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Info',
    'Task',
    'Result',
    'Optional',
    'Callable',
    'Concurrency'
]

if __name__ == '__main__':
    e = TimeoutError()
    print(type(e).__name__)
