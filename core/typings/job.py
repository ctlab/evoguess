import threading

from util.array import unzip, none
from util.collection import for_each
from util.error import AlreadyRunning, CancelledError

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

    def add_result(self, future):
        self.finished_jobs.append(future)


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

    def __enter__(self):
        for job in self.jobs:
            job._condition.acquire()

    def __exit__(self, *args):
        for job in self.jobs:
            job._condition.release()


def n_completed(jobs, count, timeout=None):
    with _AcquireJobs(jobs):
        done = set(j for j in jobs if j._state > RUNNING)
        not_done = set(jobs) - done
        count = min(count - len(done), len(not_done))

        if count > 0:
            waiter = _NCompletedWaiter(count)
            for_each(not_done, lambda j: j._waiters.append(waiter))
        else:
            return done

    waiter.event.wait(timeout)
    for job in not_done:
        with job._condition:
            job._waiters.remove(waiter)

    done.update(waiter.finished_jobs)
    return done


def first_completed(jobs, timeout=None):
    return n_completed(jobs, 1, timeout)


def all_completed(jobs, timeout=None):
    return n_completed(jobs, len(jobs), timeout)


class Job:
    def __init__(self, context, job_id):
        self.job_id = job_id

        self._indexes = []
        self._futures = []
        self._handled = []
        self._results = []
        self._waiters = []
        self._state = PENDING
        self._condition = threading.Condition()
        self._processor = threading.Thread(
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
                result = future.result(timeout=0)
                for j, index in enumerate(self._indexes[i]):
                    self._results[index] = result[j]
            except Exception as e:
                if type(e).__name__ != CANCELLED_ERROR:
                    print(f'Exception in task {i}: ', repr(e))

            self._handled[i] = True

    def _process(self, context):
        fn = context.function.get_function()
        data = context.function.prepare_data(
            context.state,
            context.instance,
            context.backdoor,
            context.dim_type,
        )
        awaiter = context.executor.get_awaiter()

        completed = []
        tasks = context.get_tasks(self._results)
        while self.running() and len(tasks) > 0:
            index_futures = context.executor.submit_all(fn, data, *tasks)
            indexes, futures = unzip(index_futures)

            is_reasonably = True
            with self._condition:
                self._indexes.extend(indexes)
                self._futures.extend(futures)
                self._results.extend(none(tasks))
                self._handled.extend(none(futures))

            active = self._get_active_futures()
            while len(active) > 0 and is_reasonably:
                count, timeout = context.get_limits(completed, len(self._results))

                for future in awaiter(active, timeout):
                    self._handle_future(future)

                active = self._get_active_futures()
                completed = self._get_completed_values()
                is_reasonably = context.is_reasonably(active, completed)

            tasks = context.get_tasks(self._results)

        with self._condition:
            if self._state == RUNNING:
                self._state = FINISHED

            for waiter in self._waiters:
                waiter.add_result(self)
            self._condition.notify_all()

    def start(self):
        if self._state != PENDING:
            raise AlreadyRunning()

        self._state = RUNNING
        self._processor.start()
        return self

    def cancel(self):
        with self._condition:
            if self._state == FINISHED:
                return False

            if self._state == RUNNING:
                self._state = CANCELLED
                for future in self._futures:
                    future.cancel()
                self._condition.notify_all()

        if self._processor is not None:
            self._processor.join()
            self._processor = None

        return True

    def cancelled(self):
        with self._condition:
            return self._state == CANCELLED

    def running(self):
        with self._condition:
            return self._state == RUNNING

    def done(self):
        with self._condition:
            return self._state > RUNNING

    def result(self, timeout):
        with self._condition:
            if self._state == CANCELLED:
                raise CancelledError()
            elif self._state == FINISHED:
                return self._results

            self._condition.wait(timeout)

            if self._state == CANCELLED:
                raise CancelledError()
            elif self._state == FINISHED:
                return self._results
            else:
                raise TimeoutError()
