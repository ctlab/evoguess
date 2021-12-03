from functools import reduce
from operator import mul
from typing import Tuple, Dict, Iterable

from method.function.types import Function
from method.sampling.types import Sampling
from numpy.random.mtrand import RandomState

from structure.array import Backdoor
from structure.data.backdoor_cache import BackdoorCache
from utils.bit_mask import apply_masks

Estimation = Dict[str, float]


def decimal_to_base(number, bases):
    values = []
    for base in bases[::-1]:
        number, value = divmod(number, base)
        values.insert(0, value)
    return values


def map_values(values, mappers):
    return [mappers[i][value] for i, value in enumerate(values)]


class Method:
    name = 'Method'

    def __init__(self,
                 output,
                 function: Function,
                 sampling: Sampling,
                 random_seed: int,
                 concurrency,
                 ):
        self.output = output
        self.sampling = sampling
        self.function = function
        self.concurrency = concurrency
        self.random_seed = random_seed

        self._active_jobs = {}
        self._permutation_cache = {}
        self._backdoor_cache = BackdoorCache(output)
        self.random_state = RandomState(seed=random_seed)

        self._max_completed_job_id = None

    def _queue(self, backdoor, task_count, offset):
        base = backdoor.base
        bd_task_count = backdoor.task_count()
        max_task_count = self.sampling.get_max()
        # generate task_dimension for current backdoor
        bd_key, bd_size = str(backdoor), len(backdoor)
        if bd_task_count > max_task_count:
            bd_masks = backdoor.get_masks()
            task_dimension = self.random_state.randint(1, base + 1, size=(task_count, bd_size))
            task_dimension = [apply_masks(values, bd_masks) for values in task_dimension]
        else:
            if bd_key in self._permutation_cache:
                task_permutation = self._permutation_cache[bd_key]
            else:
                task_permutation = self.random_state.permutation(bd_task_count)
                self._permutation_cache[bd_key] = task_permutation

            bd_bases = backdoor.get_bases()
            bd_mappers = backdoor.get_mappers()
            task_numbers = task_permutation[offset:offset + task_count]
            task_dimension = [decimal_to_base(number, bd_bases) for number in task_numbers]
            task_dimension = [map_values(values, bd_mappers) for values in task_dimension]

        # create new job for current backdoor with task_dimension
        job_f, job_tasks = self.function.get_job(backdoor, *task_dimension, random_state=self.random_state)
        job_id = self.concurrency.submit(job_f, *job_tasks, auditor=None, max_id=self._max_completed_job_id)

        self.output.debug(
            4, 2,
            '%d > %d' % (bd_task_count, max_task_count),
            'Job %d dimension:' % job_id,
            str(task_dimension)
        )

        self._active_jobs[job_id] = backdoor
        return job_id

    def queue(self, backdoor: Backdoor) -> Tuple[int, Estimation]:
        # check if job with current backdoor already exist
        bd_key = str(backdoor)
        for job_id, job_backdoor in self._active_jobs.items():
            if bd_key == str(job_backdoor):
                return -job_id, None

        # check if backdoor already estimated
        if backdoor in self._backdoor_cache:
            task_count = 0
            task_sample, estimation = self._backdoor_cache[backdoor]
            if not estimation.get('canceled', False):
                values = self.function.get_values(*task_sample)
                task_count = self.sampling.get_count(backdoor, values=values)

            if task_count == 0:
                return None, {**estimation, 'job_time': 0.}
        else:
            task_count, task_sample = self.sampling.get_count(backdoor), []
            if task_count == 0:
                raise Exception("Sample size for new backdoor can't be zero!")

        return self._queue(backdoor, task_count, len(task_sample)), None

    def _handle_job(self, job_id):
        assert job_id in self._active_jobs
        backdoor = self._active_jobs.pop(job_id)

        task_sample, _ = self._backdoor_cache.get(backdoor, ([], {}))
        task_status, task_results = self.concurrency.get(job_id)
        if task_status is None:
            return backdoor, None

        task_sample += self.function.decode_results(*task_results)
        if task_status:
            values = self.function.get_values(*task_sample)
            task_count = self.sampling.get_count(backdoor, values=values)
            if task_count > 0:
                self._backdoor_cache[backdoor] = task_sample, None
                self._queue(backdoor, task_count, len(task_sample))
                return backdoor, None

            task_sample = [task for task in task_sample if task is not None]
            statistic, estimation = self.function.calculate(backdoor, *task_sample)
        else:
            task_sample = [task for task in task_sample if task is not None]
            statistic, estimation = self.function.calculate(backdoor, *task_sample)
            estimation['canceled'] = True

        self._backdoor_cache[backdoor] = task_sample, estimation
        self._backdoor_cache.dumps(backdoor)
        return backdoor, estimation

    def wait(self, timeout=None) -> Tuple[bool, Iterable[Tuple[Backdoor, Estimation]]]:
        while True:
            requeue, estimations = False, []
            job_ids = self._active_jobs.keys()
            self._max_completed_job_id = min(job_ids) - 1
            loading, completed_jobs = self.concurrency.wait(job_ids, timeout)
            for job_id in completed_jobs:
                backdoor, estimation = self._handle_job(job_id)
                if estimation is not None:
                    estimations.append((backdoor, estimation))
                else:
                    requeue = True

            if len(estimations) > 0 or not requeue:
                break

        return loading < 1., estimations

    def __len__(self):
        return len(self.concurrency)

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.sampling,
            '-- Seed: %s' % self.random_seed,
            '--------------------',
            self.function,
            '--------------------',
            self.concurrency,
        ]))


__all__ = [
    'Method',
    'Backdoor',
]
