from .job import first_completed as fc, all_completed as ac

from util import array
from util.error import CancelledError


def first_completed(futures, timeout=None):
    done = set(f for f in futures if f.done())
    if done: return done

    jobs = fc([f.job for f in futures], timeout)
    return [f for f in futures if f.job in jobs]


def all_completed(futures, timeout=None):
    done = set(f for f in futures if f.done())
    not_done = set(futures) - done

    jobs = ac([f.job for f in not_done], timeout)
    return [f for f in futures if f in done or f.job in jobs]


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
