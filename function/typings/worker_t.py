from typing import NamedTuple, Tuple, Dict

SampleSeed = int
SampleSize = int
ChunkOffset = int
ChunkLength = int

WorkerArgs = Tuple[
    SampleSeed,
    SampleSize,
    ChunkOffset,
    ChunkLength
]

TimeMap = Dict[str, float]
ValueMap = Dict[str, float]
StatusMap = Dict[str, int]

ProcessId = int
ProcessTime = float

WorkerResult = Tuple[
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
