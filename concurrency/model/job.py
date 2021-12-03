from time import time as now

RUNNING = 'RUNNING'
CANCELLED = 'CANCELLED'
FINISHED = 'FINISHED'

TIMEOUT_ERROR = 'TimeoutError'
CANCELLED_ERROR = 'CancelledError'


class CancelledError(Exception):
    """The Job was cancelled."""

    def __init__(self, ready, results):
        self.ready = ready
        self.results = results


class TimeoutError(Exception):
    """The operation exceeded the given deadline."""
    pass


class Job:
    def __init__(self, futures):
        self._ready = 0
        self._state = RUNNING
        self._futures = futures
        self._length = len(futures)
        self._results = [None] * self._length
        self._statuses = [False] * self._length

        self._exceptions = []

    def cancel(self):
        if self._state != RUNNING:
            return False

        for future in self._futures:
            future.cancel()

        self._state = CANCELLED
        return True

    def cancelled(self):
        return self._state == CANCELLED

    def done(self):
        return self._state != RUNNING

    def result(self, timeout=0.):
        if self._state == CANCELLED:
            raise CancelledError(self._results, self._exceptions)
        if self._state == FINISHED:
            return self._results, self._exceptions

        left = self._length - self._update(timeout)
        if left == 0:
            self._state = FINISHED
            return self._results, self._exceptions
        else:
            raise TimeoutError()

    def update(self):
        if self._state in [CANCELLED, FINISHED]:
            return 0
        return self._length - self._update()

    def _set(self, i, result):
        self._results[i] = result
        self._statuses[i] = True

    def _unresolved(self):
        return [i for i, status in enumerate(self._statuses) if not status]

    def _update(self, timeout=0.):
        wall_time = now() + timeout
        for i in self._unresolved():
            future = self._futures[i]
            if future.cancelled():
                self._set(i, None)
                continue

            try:
                job_timeout = wall_time - now()
                if future.done():
                    self._set(i, future.result())
                elif job_timeout > 0:
                    self._set(i, future.result(job_timeout))
                else:
                    break
            except Exception as e:
                name = type(e).__name__
                if name == TIMEOUT_ERROR:
                    break

                self._set(i, None)
                if name != CANCELLED_ERROR:
                    self._exceptions.append((i, e))

        self._ready = sum(self._statuses)
        return self._ready


__all__ = [
    'Job',
    'TimeoutError',
    'CancelledError'
]
