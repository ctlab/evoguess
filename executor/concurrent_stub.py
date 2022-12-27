from time import time as now, sleep
from numpy.random import randint

from util.caster import inf_none


class JobStub:
    def __init__(self, times, thread_map):
        self.times = times
        self.thread_map = thread_map

        self.max_time = 0
        self.end_stamp = None
        self.start_stamp = now()
        for thread, thread_times in self.thread_map.items():
            thread_time = sum(thread_times)
            if thread_time > self.max_time:
                self.max_time = thread_time

    def result(self, timeout=None):
        left = self.max_time + self.start_stamp - now()
        if timeout and left > timeout:
            sleep(timeout)
            raise TimeoutError
        else:
            sleep(left)

        self.end_stamp = self.end_stamp if self.end_stamp else now()
        return [
            (i, 0, False, 10 * time, 105 * time, 86 * time, 94 * time, time, 0, 0)
            for i, time in enumerate(self.times)
        ]
        # return [
        #     (i, 0, False, {
        #         'restarts': 10 * time,
        #         'conflicts': 105 * time,
        #         'decisions': 86 * time,
        #         'propagations': 94 * time,
        #         'time': time
        #     }, 0, 0) for i, time in enumerate(self.times)
        # ]

    def cancel(self):
        left = self.max_time + self.start_stamp - now()
        self.end_stamp = self.end_stamp if self.end_stamp else now()
        return True if left > 0 else False, []

    def done(self):
        left = self.max_time + self.start_stamp - now()
        return left <= 0


class ConcurrentStub:
    def __init__(self):
        self.threads = 36

    def _get_min_thread(self, thread_map):
        min_thread, min_time = -1, None
        for thread, thread_times in thread_map.items():
            thread_time = sum(thread_times)
            if min_time is None or thread_time < min_time:
                min_thread = thread
                min_time = thread_time
        return min_thread

    def submit(self, func, *tasks):
        times = [x / 10. for x in randint(1, 11, size=(len(tasks),))]
        thread_map = {i: [] for i in range(self.threads)}
        for time in times:
            thread = self._get_min_thread(thread_map)
            thread_map[thread].append(time)
        return JobStub(times, thread_map)
