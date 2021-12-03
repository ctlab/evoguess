from time import time as now

RUNNING = 'RUNNING'
CANCELLED = 'CANCELLED'
FINISHED = 'FINISHED'

TIMEOUT_ERROR = 'TimeoutError'
CANCELLED_ERROR = 'CancelledError'


class CancelledError(Exception):
    """The Job was cancelled."""
    pass


class TimeoutError(Exception):
    """The operation exceeded the given deadline."""
    pass


class Job:
    def __init__(self, length):
        self._state = RUNNING
        self._length = length

        self._exceptions = []
        self._results = [None] * length
        self._statuses = [False] * length

    def _unresolved(self):
        for i, status in enumerate(self._statuses):
            if not status:
                yield i

    def _cancel(self):
        raise NotImplementedError

    def _update_state(self):
        raise NotImplementedError

    def cancel(self):
        self._update_state()
        if self._state != RUNNING:
            return False

        self._cancel()
        self._state = CANCELLED
        return True

    def cancelled(self):
        self._update_state()
        return self._state == CANCELLED

    def done(self):
        self._update_state()
        return self._state != RUNNING

    def result(self, timeout=None):
        self._update_state()
        if self._state == CANCELLED:
            raise CancelledError()
        elif self._state == FINISHED:
            return self._results, self._exceptions

        self.wait(0, timeout)

        if self._state == CANCELLED:
            raise CancelledError()
        elif self._state == FINISHED:
            return self._results, self._exceptions
        else:
            raise TimeoutError()

    def partial_result(self):
        pass

    def wait(self, count, timeout=None):
        raise NotImplementedError

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

        return self._length - sum(self._statuses)


__all__ = [
    'Job',

    'RUNNING',
    'CANCELLED',
    'FINISHED',

    'TimeoutError',
    'CancelledError',
]
