from .job import first_completed as fc

from util import array
from util.error import CancelledError


def first_completed(futures, timeout=None):
    # todo: return done and not_done
    done = [f for f in futures if isinstance(f, EstimationFuture)]
    if done: return done

    jobs = fc([f.job for f in futures], timeout)
    return done or [future for future in futures if future.job in jobs]


class MethodFuture:
    def __init__(self, job):
        self.job = job
        self.context = job.context

    def _process(self, cases, canceled):
        results = array.trim(cases)
        del self.context.cache.active[self.context.backdoor]
        values = self.context.function.get_values(*results)
        estimation = {
            **self.context.sampling.report(values),
            **self.context.function.calculate(self.context.backdoor, *results)
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


class EstimationFuture:
    def __init__(self, estimation):
        self.estimation = estimation

    def result(self, timeout=None):
        return {**self.estimation, 'job_time': 0}

    def cancel_and_result(self):
        return {**self.estimation, 'job_time': 0}


__all__ = [
    'MethodFuture',
    'EstimationFuture',
    #
    'first_completed',
]
