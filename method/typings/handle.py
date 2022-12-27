from .job import n_completed as nc

from util.collection import trim
from util.error import CancelledError


def n_completed(handles, count, timeout=None):
    done = [h for h in handles if h.done()]

    if count > len(done):
        not_done = set(handles) - set(done)
        count = min(count - len(done), len(not_done))
        jobs = nc([h.job for h in not_done], count, timeout)
        return [h for h in handles if h in done or h.job in jobs]
    else:
        return done


class Handle:
    def done(self):
        raise NotImplementedError

    def result(self, timeout=None):
        raise NotImplementedError

    def cancel_and_result(self):
        raise NotImplementedError


class JobHandle(Handle):
    def __init__(self, job):
        self.job = job
        self.context = job.context

    def _process(self, cases, canceled):
        results = trim(cases)
        del self.context.cache.active[self.context.backdoor]
        # values = self.context.function.get_values(*results)
        estimation = {
            'list_seed': self.context.state['list_seed'],
            'func_seed': self.context.state['func_seed'],
            # **self.context.sampling.report(values),
            **self.context.function.calculate(self.context.backdoor, *results),
        }
        # todo: separate result and estimation
        results = []
        if canceled:
            estimation['value'] = float('inf')
            self.context.cache.canceled[self.context.backdoor] = results, estimation
        else:
            self.context.cache.estimated[self.context.backdoor] = results, estimation

        return estimation

    def done(self):
        return self.job.done()

    def result(self, timeout=None):
        try:
            cases = self.job.result(timeout)
            return self._process(cases, False)
        except CancelledError:
            return self._process([], True)

    def cancel_and_result(self):
        if self.job.cancel():
            return self._process([], True)
        else:
            return self._process(self.job._results, False)


class VoidHandle(Handle):
    def __init__(self, estimation):
        self._estimation = estimation

    def done(self):
        return True

    def result(self, timeout=None):
        return self._estimation

    def cancel_and_result(self):
        return self._estimation


__all__ = [
    'Handle',
    'JobHandle',
    'VoidHandle',
    #
    'n_completed',
]
