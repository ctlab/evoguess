import threading

from enum import Enum
from typing import Optional

from util.array import unzip, none
from util.collection import for_each
from util.error import AlreadyRunning, CancelledError

Timeout = Optional[int]


class JobState(Enum):
    [
        PENDING,
        RUNNING,
        FINISHED,
        CANCELLED
    ] = range(4)


TIMEOUT_ERROR = 'TimeoutError'
CANCELLED_ERROR = 'CancelledError'


class _Waiter(object):
    def __init__(self):
        self.finished_jobs = []
        self.event = threading.Event()

    def add_result(self, job):
        self.finished_jobs.append(job)


class _NCompletedWaiter(_Waiter):
    def __init__(self, pending_calls):
        super().__init__()
        self.lock = threading.Lock()
        self.pending_calls = pending_calls

    def _decrement_pending_calls(self):
        with self.lock:
            self.pending_calls -= 1
            if not self.pending_calls:
                self.event.set()

    def add_result(self, job):
        super().add_result(job)
        self._decrement_pending_calls()


class _AcquireJobs(object):
    def __init__(self, jobs):
        self.jobs = sorted(jobs, key=id)

    # noinspection PyProtectedMember
    def __enter__(self):
        for job in self.jobs:
            job._condition.acquire()

    # noinspection PyProtectedMember
    def __exit__(self, *args):
        for job in self.jobs:
            job._condition.release()


class Job:
    def __init__(self, context, job_id):
        self.job_id = job_id
        self.context = context

        self._indexes = []
        self._futures = []
        self._handled = []
        self._results = []
        self._waiters = []
        self._state = JobState.PENDING
        self._condition = threading.Condition()
        self._job_manager = threading.Thread(
            name=f'JobManagerThread {job_id}',
            target=self._process, args=(context,)
        )

    def _get_active_futures(self):
        return [
            self._futures[i]
            for i in range(len(self._handled))
            if not self._handled[i]
        ]

    def _get_completed_values(self):
        # todo: avoid index getting
        return [result[2] for result in self._results if result]

    def _handle_future(self, future, i=None):
        with self._condition:
            i = i or self._futures.index(future)
            try:
                results = future.result(timeout=0)
                for j, index in enumerate(self._indexes[i]):
                    self._results[index] = results[j]
            except Exception as e:
                if type(e).__name__ != CANCELLED_ERROR:
                    print(f'Exception in task {i}: ', repr(e))

            self._handled[i] = True

    def _process(self, context):
        fn = context.function.get_function()
        awaiter = context.executor.get_awaiter()
        payload = context.function.get_payload(
            context.instance, context.backdoor
        )

        completed = []
        tasks = context.get_tasks(self._results)
        while self.running() and len(tasks) > 0:
            index_futures = context.executor.submit_all(fn, payload, tasks)
            indexes, futures = unzip(index_futures)

            is_reasonably = True
            with self._condition:
                self._indexes.extend(indexes)
                self._futures.extend(futures)
                self._results.extend(none(tasks))
                self._handled.extend(none(futures))

            active = self._get_active_futures()
            while len(active) > 0 and is_reasonably:
                count, timeout = context.get_limits(self._results)

                for future in awaiter(active, timeout):
                    self._handle_future(future)

                active = self._get_active_futures()
                # completed = self._get_completed_values()
                is_reasonably = context.is_reasonably(active, self._results)

            tasks = context.get_tasks(self._results)

        with self._condition:
            if self._state == JobState.RUNNING:
                self._state = JobState.FINISHED

            for waiter in self._waiters:
                waiter.add_result(self)
            self._condition.notify_all()

    def start(self) -> 'Job':
        if self._state != JobState.PENDING:
            raise AlreadyRunning()

        self._state = JobState.RUNNING
        self._job_manager.start()
        return self

    def cancel(self) -> bool:
        with self._condition:
            if self._state == JobState.FINISHED:
                return False

            if self._state == JobState.RUNNING:
                self._state = JobState.CANCELLED
                for future in self._futures:
                    future.cancel()
                self._condition.notify_all()

        if self._job_manager is not None:
            self._job_manager.join()
            self._job_manager = None

        return True

    def done(self) -> bool:
        with self._condition:
            return self._state > JobState.RUNNING

    def running(self) -> bool:
        with self._condition:
            return self._state == JobState.RUNNING

    def cancelled(self) -> bool:
        with self._condition:
            return self._state == JobState.CANCELLED

    def result(self, timeout: Timeout) -> object:
        with self._condition:
            if self._state == JobState.CANCELLED:
                raise CancelledError()
            elif self._state == JobState.FINISHED:
                return self._results

            self._condition.wait(timeout)

            if self._state == JobState.CANCELLED:
                raise CancelledError()
            elif self._state == JobState.FINISHED:
                return self._results
            else:
                raise TimeoutError()


# noinspection PyProtectedMember
def n_completed(jobs: list[Job], count: int, timeout: Timeout = None) -> list[Job]:
    with _AcquireJobs(jobs):
        done = set(j for j in jobs if j._state > JobState.RUNNING)
        not_done = set(jobs) - done
        count = min(count - len(done), len(not_done))

        if count > 0:
            waiter = _NCompletedWaiter(count)
            for_each(not_done, lambda j: j._waiters.append(waiter))
        else:
            return list(done)

    waiter.event.wait(timeout)
    for job in not_done:
        with job._condition:
            job._waiters.remove(waiter)

    done.update(waiter.finished_jobs)
    return list(done)


def all_completed(jobs: list[Job], timeout: Timeout = None) -> list[Job]:
    return n_completed(jobs, len(jobs), timeout)


def first_completed(jobs: list[Job], timeout: Timeout = None) -> list[Job]:
    return n_completed(jobs, 1, timeout)


__all__ = [
    'Job',
    # waiters
    'n_completed',
    'all_completed',
    'first_completed',
]
