from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from numpy import ndarray


@dataclass
class Line:
    """data that is common to a certain group of data"""
    y: ndarray
    axis: int
    line: Line2D

    def __hash__(self):
        return hash((str(self.y), self.line))
