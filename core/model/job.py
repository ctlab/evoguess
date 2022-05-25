import threading

from enum import Enum
from typing import Optional

from util.array import none
from util.collection import for_each
from function.typings import ChunkResults as Res
from typings.future import Future, AcquireFutures
from util.error import AlreadyRunning, CancelledError

Timeout = Optional[int]


class JobState(Enum):
    [
        PENDING,
        RUNNING,
        FINISHED,
        CANCELLED
    ] = range(4)


class JobException(Exception):
    def __init__(self, exceptions):
        self.exceptions = exceptions


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


class Job(Future):
    def __init__(self, context, job_id):
        self.job_id = job_id
        self.context = context

        self._futures = []
        self._results = []
        self._waiters = []
        self._exceptions = []
        self._state = JobState.PENDING
        self._condition = threading.Condition()
        self._job_manager = threading.Thread(
            name=f'JobManagerThread {job_id}',
            target=self._process, args=(context,)
        )

    def _process(self, context):
        fn = context.function.get_function()
        payload = context.function.get_payload(
            context.instance, context.backdoor
        )

        tasks = context.get_tasks(self._results)
        iterables = [(args, payload) for args in tasks]
        while self.running() and len(iterables) > 0:
            future_all = context.executor.submit_all(fn, *iterables)

            is_reasonably = True
            with self._condition:
                self._futures.append(future_all)
                self._results.extend(none(iterables))

            while len(future_all) > 0 and is_reasonably:
                for future in future_all.as_complete():
                    with self._condition:
                        if future._exception is not None:
                            self._exceptions.append(future._exception)
                        elif future._result is not None:
                            idx = self._futures.index(None)
                            self._results[idx] = Res(*future._result)

            tasks = context.get_tasks(self._results)
            iterables = [(args, payload) for args in tasks]

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

    def add_done_callback(self, fn):
        pass

    # noinspection DuplicatedCode
    def result(self, timeout: Timeout = None) -> object:
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

    # noinspection DuplicatedCode
    def exception(self, timeout: Timeout = None) -> Exception:
        with self._condition:
            if self._state == JobState.CANCELLED:
                raise CancelledError()
            elif self._state == JobState.FINISHED:
                return JobException(self._exceptions)

            self._condition.wait(timeout)

            if self._state == JobState.CANCELLED:
                raise CancelledError()
            elif self._state == JobState.FINISHED:
                return JobException(self._exceptions)
            else:
                raise TimeoutError()


# noinspection PyProtectedMember
def n_completed(jobs: list[Job], count: int, timeout: Timeout = None) -> list[Job]:
    with AcquireFutures(*jobs):
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
