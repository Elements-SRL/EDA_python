from dataclasses import dataclass
from typing import Dict

from numpy import ndarray


@dataclass
class MetaData:
    id: int
    x: ndarray
    ch_to_sweep: Dict[int, ndarray]
    y: ndarray
    channelCount: int
    sweepNumber: int
    visible: bool = True
    sweepUnitsC: str = "mV"
    sweepUnitsX: str = "sec"
    sweepUnitsY: str = "nA"
    labelC = ""
