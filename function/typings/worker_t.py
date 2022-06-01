from typing import Optional, NamedTuple

SampleSeed = int
SampleSize = int
ChunkOffset = int
ChunkLength = int

WorkerArgs = tuple[
    SampleSeed,
    SampleSize,
    ChunkOffset,
    ChunkLength
]

TimeMap = dict[str, float]
ValueMap = dict[str, float]
StatusMap = dict[str, int]

ProcessId = int
ProcessTime = float

WorkerResult = tuple[
    TimeMap,
    ValueMap,
    StatusMap,
    WorkerArgs,
    ProcessId,
    ProcessTime,
]


class ChunkResult(NamedTuple):
    times: TimeMap
    values: ValueMap
    statuses: StatusMap
    arguments: WorkerArgs
    # process info
    pid: ProcessId
    ptime: ProcessTime


__all__ = [
    'WorkerArgs',
    'ChunkResult',
    'WorkerResult',
]
