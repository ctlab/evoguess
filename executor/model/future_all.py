import time
import threading

from typings.future import Future
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


# noinspection PyProtectedMember
class FutureAll:
    def __init__(self, futures: list[Future]):
        self._futures = set(futures)
        self._tracker = _Tracker(futures)

    def _release_futures(self):
        with self._tracker.lock:
            finished = self._tracker.finished_futures
            self._tracker.finished_futures = []
            self._tracker.event = None
        self._futures -= set(finished)

        for future in finished:
            with future._condition:
                future._waiters.remove(self._tracker)
        return finished

    # noinspection PyProtectedMember
    def as_complete(self, count: Uint = None, timeout: Float = None):
        assert self._tracker.event is None, "not thread safety!"
        assert count is None or count >= 0, "not uint!"
        count = count or len(self._futures)

        if timeout is not None:
            if timeout <= 0:
                return self._release_futures()
            end_time = timeout + time.time()

        count = count or len(self._futures)
        with self._tracker.lock:
            if count > len(self._tracker.finished_futures):
                self._tracker.event = threading.Event()
                self._tracker.pending_calls = min(
                    self._tracker.pending_futures,
                    count - len(self._tracker.finished_futures)
                )

        if self._tracker.event:
            if timeout is not None:
                timeout = end_time - time.time()
            self._tracker.event.wait(timeout)

        return self._release_futures()

    @property
    def pending_futures(self) -> int:
        return self._tracker.pending_futures


__all__ = [
    'FutureAll'
]
