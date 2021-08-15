from .job import n_completed as nc

from util import array
from util.error import CancelledError


def n_completed(handles, count, timeout=None):
    done = set(h for h in handles if h.done())
    count = min(count, len(handles))
    if len(done) >= count:
        return done

    not_done = set(handles) - done
    jobs = nc([h.job for h in not_done], count, timeout)
    return [h for h in handles if h in done or h.job in jobs]


class Handle:
    def __init__(self, done=False):
        self._done = done

    def done(self):
        return self._done

    def result(self, timeout=None):
        raise NotImplementedError

    def cancel_and_result(self):
        raise NotImplementedError


class JobHandle(Handle):
    def __init__(self, job):
        super().__init__()
        self.job = job
        self.context = job.context

    def _process(self, cases, canceled):
        self._done = True
        results = array.trim(cases)
        del self.context.cache.active[self.context.backdoor]
        # values = self.context.function.get_values(*results)
        estimation = {
            'list_seed': self.context.state['list_seed'],
            'func_seed': self.context.state['func_seed'],
            # **self.context.sampling.report(values),
            **self.context.function.calculate(self.context.backdoor, *results),
        }
        if canceled:
            estimation['value'] = float('inf')
            self.context.cache.canceled[self.context.backdoor] = results, estimation
        else:
            self.context.cache.estimated[self.context.backdoor] = results, estimation

        return estimation

    def result(self, timeout=None):
        try:
            cases = self.job.result(timeout)
        except CancelledError:
            cases = self.job._results
            self.job.join()

        return self._process(cases, False)

    def cancel_and_result(self):
        if not self.job.cancel():
            self.job.join()
        return self._process(self.job._results, True)


class VoidHandle(Handle):
    def __init__(self, estimation):
        super().__init__()
        self._done = True
        self._estimation = estimation

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
