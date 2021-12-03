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


class MultiJob:
    def __init__(self, futures, future_index):
        self._ready = 0
        self._state = RUNNING
        self._futures = futures
        self._future_index = future_index
        self._length = sum(map(len, future_index))

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

    def _set(self, index, result):
        for i, j in enumerate(index):
            self._statuses[j] = True
            self._results[j] = None if result is None else result[i]

    def _update(self, timeout=0.):
        i, wall_time = 0, now() + timeout
        while i < len(self._futures):
            future, index = self._futures[i], self._future_index[i]
            if future.cancelled():
                self._set(index, None)
                continue

            try:
                job_timeout = wall_time - now()
                if future.done():
                    self._set(index, future.result())
                elif job_timeout > 0:
                    self._set(index, future.result(job_timeout))
                else:
                    break

                self._futures.pop(i)
                self._future_index.pop(i)
            except Exception as e:
                name = type(e).__name__
                if name == TIMEOUT_ERROR:
                    break

                self._set(index, None)
                self._futures.pop(i)
                self._future_index.pop(i)

                if name != CANCELLED_ERROR:
                    self._exceptions.append((i, e))

        self._ready = sum(self._statuses)
        return self._ready


__all__ = [
    'MultiJob',
    'TimeoutError',
    'CancelledError'
]
