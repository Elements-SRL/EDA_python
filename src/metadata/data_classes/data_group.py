from dataclasses import dataclass, field
from typing import Set, List

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
    basic_data: OrderedSet[BasicData] = OrderedSet()
    id: int = -1

    def __hash__(self):
        return hash((self.id, str(self.x), self.sampling_rate, self.channel_count, self.sweep_count,
                     self.measuring_unit, frozenset(self.basic_data)))


def make_copy(dg: DataGroup, new_id: int) -> DataGroup:
    return DataGroup(x=dg.x,
                     sampling_rate=dg.sampling_rate,
                     channel_count=dg.channel_count,
                     sweep_count=dg.sweep_count,
                     measuring_unit=dg.measuring_unit,
                     sweep_label_x=dg.sweep_label_x,
                     sweep_label_y=dg.sweep_label_y,
                     sweep_label_c=dg.sweep_label_c,
                     data_groups=set(),
                     basic_data=dg.basic_data,
                     id=new_id,
                     name=dg.name,
                     type=dg.type,
                     )
