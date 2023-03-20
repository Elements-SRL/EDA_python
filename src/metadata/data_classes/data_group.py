from dataclasses import dataclass, field
from typing import Set
import copy
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
    name: str
    type: str
    data_groups: Set = field(default_factory=set)
    basic_data: OrderedSet[BasicData] = field(default_factory=OrderedSet)
    id: int = -1

    def __hash__(self):
        return hash((self.id, str(self.x), self.sampling_rate, self.channel_count, self.sweep_count,
                     self.measuring_unit, frozenset(self.basic_data)))


def make_copy(dg: DataGroup, new_id: int) -> DataGroup:
    copied = copy.deepcopy(dg)
    copied.id = new_id
    return copied


def empty_dg_from(dg: DataGroup, new_id: int) -> DataGroup:
    copied = copy.deepcopy(dg)
    copied.id = new_id
    copied.basic_data = OrderedSet()
    return copied
