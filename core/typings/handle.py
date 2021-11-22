from .job import n_completed as nc

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

    def cancel(self):
        raise NotImplementedError

    def result(self, timeout=None):
        raise NotImplementedError


class JobHandle(Handle):
    def __init__(self, point, job):
        self.job = job
        self.point = point

    def done(self):
        return self.job.done()

    def cancel(self):
        return self.job.cancel()

    def result(self, timeout=None):
        try:
            estimation = self.job.result(timeout)
            return self.point.set(**estimation)
        except CancelledError:
            return self.point


class VoidHandle(Handle):
    def __init__(self, estimated):
        self.estimated = estimated

    def done(self):
        return True

    def cancel(self):
        return False

    def result(self, timeout=None):
        return self.estimated


__all__ = [
    'Handle',
    'JobHandle',
    'VoidHandle',
    #
    'n_completed',
]
