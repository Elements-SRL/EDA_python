from typing import Set, List, Dict, Tuple

from numpy import ndarray

from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import CommonData


class MetaData:

    def __init__(self):
        self.common_data: CommonData | None = None
        self.data: Set[BasicData] = set()

    def get_x(self) -> ndarray:
        return self.common_data.x

    def get_channel_y(self, channel: int) -> List[ndarray]:
        return [d.y for d in self.data if d.ch == channel]

    def get_all_y(self) -> List[Tuple[int, List[ndarray]]]:
        d = {ch: self.get_channel_y(ch) for ch in range(self.common_data.channel_count)}
        return list(zip(d.keys(), d.values()))

    def add_data(self, basic_data: BasicData):
        self.data.add(basic_data)

    def add_common_data(self, cd: CommonData):
        # if cd != self.common_data:
        self.common_data = cd

    def get_visible_data(self):
        return [d for d in self.data if d.visible]

    def is_empty(self):
        return len(self.data) == 0 or self.common_data is None

    def set_visibility(self, name: str, visibility: bool):
        for d in self.data:
            if d.name == name:
                d.visible = visibility
