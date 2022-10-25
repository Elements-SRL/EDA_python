from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class FittingParams:
    """Fitting params"""
    ch: int
    measuring_unit: str
    popt: List[Tuple[str, float]]
