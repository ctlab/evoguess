import time
import threading

from typings.optional import Uint, Float

NOTIFIED_STATES = [
    'FINISHED',
    'CANCELLED_AND_NOTIFIED'
]


# noinspection PyProtectedMember
class _AcquireFutures(object):
    def __init__(self, futures):
        self.futures = sorted(futures, key=id)

    def __enter__(self):
        for future in self.futures:
            future._condition.acquire()

    def __exit__(self, *args):
        for future in self.futures:
            future._condition.release()


class _Tracker:
    # noinspection PyProtectedMember
    def __init__(self, futures):
        self.event = None
        self.pending_calls = 0
        self.finished_futures = []
        self.lock = threading.Lock()

        with _AcquireFutures(futures):
            self.pending_futures = 0
            for future in futures:
                if future._state in NOTIFIED_STATES:
                    self.finished_futures.append(future)
                else:
                    self.pending_futures += 1
                    future._waiters.append(self)

    def release_futures(self):
        with self.lock:
            finished = self.finished_futures
            self.finished_futures = []
            self.event = None
        return finished

    def _decrement_pending_calls(self):
        if self.event:
            self.pending_calls -= 1
            if not self.pending_calls:
                self.event.set()

    def add_result(self, future):
        with self.lock:
            self.pending_futures -= 1
            self._decrement_pending_calls()
            self.finished_futures.append(future)

    def add_exception(self, future):
        with self.lock:
            self.pending_futures -= 1
            self._decrement_pending_calls()
            self.finished_futures.append(future)

    def add_cancelled(self, future):
        with self.lock:
            self.pending_futures -= 1
            self._decrement_pending_calls()
            self.finished_futures.append(future)


class FutureBox:
    def __init__(self, futures):
        self._futures = set(futures)
        self._tracker = _Tracker(futures)

    # noinspection PyProtectedMember
    def as_complete(self, count: Uint = None, timeout: Float = None):
        if timeout is not None:
            if timeout <= 0:
                return self._tracker.release_futures()
            end_time = timeout + time.time()

        assert count is None or count >= 0
        count = count or len(self._futures)
        with self._tracker.lock:
            if count > len(self._tracker.finished_futures):
                assert self._tracker.event is None
                self._tracker.event = threading.Event()
                self._tracker.pending_calls = min(
                    self._tracker.pending_futures,
                    count - len(self._tracker.finished_futures)
                )

        if self._tracker.event:
            if timeout is not None:
                timeout = end_time - time.time()
            self._tracker.event.wait(timeout)

        finished = self._tracker.release_futures()
        for future in finished:
            with future._condition:
                future._waiters.remove(self._tracker)
        self._futures -= set(finished)

        return finished

    def loaded(self) -> int:
        return len(self._futures)


__all__ = [
    'FutureBox'
]
