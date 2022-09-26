from dataclasses import dataclass

from numpy import ndarray


@dataclass
class CommonData:
    """data that are common to all loaded data"""
    x: ndarray = ndarray([])
    sampling_rate: float = 0
    channel_count: int = 0
    # measuring units
