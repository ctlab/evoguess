from ..concurrency import *
from ..model.multi_job import *
from method.solver.impl.pysat import PySat

try:
    from mpi4py import MPI
    from mpi4py.futures import ProcessPoolExecutor
except ModuleNotFoundError:
    pass

from time import time as now, sleep


def multi_f(f, tasks, ids):
    job_id, max_id = ids
    if max_id is not None:
        PySat.clear(max_id)
    return [f(*args, key=job_id) for args in tasks]


class MPIExecutor(Concurrency):
    name = "Concurrency: MPI Executor"

    def __init__(self, *args, **kwargs):
        self.jobs = {}
        self.counter = 0
        self.tick = kwargs.get('tick', 0.1)
        self.workload = kwargs.get('workload', 0.9)
        self.multi_rate = kwargs.get('multi_rate', 4)
        self.debug_ticks = kwargs.get('debug_ticks', 100)

        super().__init__(*args, **kwargs)
        self.mpi_size = MPI.COMM_WORLD.Get_size()
        self.executor = ProcessPoolExecutor(len(self))

    def submit(self, f: Callable, *tasks: Task, auditor=None, max_id=None) -> Optional[int]:
        if len(tasks) == 0:
            return None

        self.counter += 1
        job_id = self.counter
        assert job_id not in self.jobs

        # futures = []
        # for args in tasks:
        #     future = self.executor.submit(f, *args)
        #     futures.append(future)
        #
        # self.jobs[job_id] = Job(futures), auditor
        # return job_id

        count = len(tasks)
        futures, future_index = [], []
        task_permutation = self.random_state.permutation(count)
        size = max(1, int(count // (self.multi_rate * len(self))))
        for i in range(0, count, size):
            index = task_permutation[i:i + size]
            multi_tasks = tuple(tasks[j] for j in index)
            future = self.executor.submit(multi_f, f, multi_tasks, (job_id, max_id))

            futures.append(future)
            future_index.append(index)

        self.jobs[job_id] = MultiJob(futures, future_index), auditor
        return job_id

    def cancel(self, job_id: int) -> Optional[bool]:
        try:
            job, _ = self.jobs.pop(job_id)
            return job.cancel()
        except KeyError:
            return None

    def _update_jobs(self, jobs, debug=False):
        ready, all_left = [], 0
        for job_id, (job, auditor) in jobs.items():
            if job is None:
                continue

            job_left = job.update()
            if job_left == 0:
                ready.append(job_id)
                continue

            if auditor and not auditor(job):
                if self.cancel(job_id) is not None:
                    ready.append(job_id)
                    continue

            all_left += job_left

        for job_id in ready:
            jobs[job_id] = (None, None)

        if debug:
            self.output.debug(3, 1, 'Left %d task(s) of %d job(s)' % (all_left, len(self.jobs)))

        return ready, float(all_left) / len(self)

    def wait(self, job_ids, timeout: float = None) -> Info:
        if timeout is None:
            wall_time = float('inf')
        else:
            wall_time = now() + max(timeout, self.tick)

        i = 0
        jobs = {key: self.jobs.get(key, (None, None)) for key in job_ids}
        ready, loading = self._update_jobs(jobs)
        while wall_time > now():
            if len(ready) > 0 or loading < self.workload:
                break

            sleep(self.tick)
            i = (i + 1) % self.debug_ticks
            ready, loading = self._update_jobs(jobs, debug=(i == 0))

        return loading, ready

    def get(self, job_id: int) -> Result:
        if job_id not in self.jobs:
            raise KeyError

        job, auditor = self.jobs.pop(job_id)
        try:
            result, exceptions = job.result()
            for i, e in exceptions:
                self.output.error(self.name, 'Exception from job %d of task %d' % (job_id, i), e)

            return True, result
        except TimeoutError:
            self.jobs[job_id] = job, auditor
            return None, None
        except CancelledError as e:
            percent = 100.0 * e.ready / len(e.results)
            self.output.debug(1, 1, 'Job %d has been canceled (%d%%)' % (job_id, percent))
            return False, e.results

    def shutdown(self, wait=True):
        self.executor.shutdown(wait)

    def __len__(self):
        return max(1, self.mpi_size - 1)

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            '-- MPI size: %d' % self.mpi_size,
            '-- Seed: %s' % self.random_seed,
            '-- Tick: %.2f' % self.tick,
            '-- Workload: %.2f' % self.workload,
        ]))


__all__ = [
    'MPIExecutor'
]
