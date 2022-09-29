from dataclasses import dataclass
from enum import Enum
from numpy import ndarray


class SweepType(Enum):
    episodic = 1
    gap_free = 2


@dataclass
class CommonData:
    """data that is common to all loaded data"""
    x: ndarray
    sampling_rate: float
    channel_count: int
    sweep_type: SweepType
    measuring_unit: str
