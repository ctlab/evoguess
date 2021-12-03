from ..job import *


class MPIFutures(Job):
    def __init__(self, futures):
        self._futures = futures
        super().__init__(len(futures))

    def _update_state(self):
        if self._state in [CANCELLED, FINISHED]:
            return

        for i in self._unresolved():
            future = self._futures[i]

    def _cancel(self):
        for future in self._futures:
            future.cancel()

    def wait(self, count, timeout=None):
        pass
