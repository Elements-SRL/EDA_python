from dataclasses import dataclass
from numpy import ndarray
from ordered_set import OrderedSet

from src.metadata.data_classes.basic_data import BasicData


@dataclass
class DataGroup:
    """data that is common to a certain group of data"""
    x: ndarray
    sampling_rate: float
    channel_count: int
    sweep_count: int
    measuring_unit: str
    sweep_label_x: str
    sweep_label_y: str
    sweep_label_c: str
    basic_data: OrderedSet[BasicData] = OrderedSet()
    id: int = -1

    def __hash__(self):
        return hash((self.id, str(self.x), self.sampling_rate, self.channel_count, self.sweep_count,
                     self.measuring_unit, frozenset(self.basic_data)))
