from dataclasses import dataclass

from numpy import ndarray


@dataclass
class CommonData:
    """data that are common to all loaded data"""
    x: ndarray
    sampling_rate: float
    channel_count: int
    # measuring units
