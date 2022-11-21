from typing import NamedTuple, Tuple, Dict, List

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

ProcessId = int
ProcessTime = float

TimeMap = Dict[str, float]
ValueMap = Dict[str, float]
StatusMap = Dict[str, int]

WorkerResult = Tuple[
    ProcessId,
    ProcessTime,
    # main info
    TimeMap,
    ValueMap,
    StatusMap,
    WorkerArgs,
]


class ChunkResult(NamedTuple):
    pid: ProcessId
    ptime: ProcessTime
    # main info
    times: TimeMap
    values: ValueMap
    statuses: StatusMap
    arguments: WorkerArgs


Results = List[ChunkResult]

__all__ = [
    'Results',
    'TimeMap',
    'ValueMap',
    'StatusMap',
    'WorkerArgs',
    'ChunkResult',
    'WorkerResult',
]
