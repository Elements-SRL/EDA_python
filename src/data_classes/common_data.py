from dataclasses import dataclass
from numpy import ndarray


@dataclass
class CommonData:
    """data that is common to all loaded data"""
    x: ndarray
    sampling_rate: float
    channel_count: int
    sweep_count: int
    measuring_unit: str
    sweep_label_x: str
    sweep_label_y: str
    sweep_label_c: str
