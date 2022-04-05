from typing import Optional

TaskId = int
TaskTime = float
TaskValue = float
TaskStatus = Optional[bool]

ProcessId = int
ProcessTime = float

Result = tuple[
    TaskId,
    TaskTime,
    TaskValue,
    TaskStatus,
    ProcessId,
    ProcessTime,
]


class TaskResult:
    def __init__(self, result: Result):
        [
            self.id,
            self.time,
            self.value,
            self.status,
            self.pid,
            self.ptime
        ] = result


__all__ = [
    'Result',
    'TaskId',
    'TaskResult'
]
