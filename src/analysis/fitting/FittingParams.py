from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class FittingParams:
    """Fitting params

    Constructor params
    ------------------
    ch: int
        channels for which the params have been found
    measuring_unit: str
        measuring unit of channel
    popt: List[Tuple[str, float]]
        optimal parameters that approximate the data
    """
    ch: int
    measuring_unit: str
    popt: List[Tuple[str, float]]
