from typing import Set, List, Dict, Tuple

from numpy import ndarray

from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import CommonData


class MetaData:

    def __init__(self):
        self.common_data: CommonData | None = None
        self.data: Set[BasicData] = set()
        self.paths: Set[str] = set()

    def clear(self):
        self.data.clear()
        self.common_data = None
        self.paths.clear()

    def get_x(self) -> ndarray:
        return self.common_data.x

    def get_channel_y(self, channel: int) -> List[ndarray]:
        return [d.y for d in self.data if d.ch == channel]

    def get_all_y(self) -> List[Tuple[int, List[ndarray]]]:
        d = {ch: self.get_channel_y(ch) for ch in range(self.common_data.channel_count)}
        return list(zip(d.keys(), d.values()))

    def add_data(self, basic_data: BasicData):
        if basic_data not in self.data:
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

    def add_path(self, path_to_file):
        self.paths.add(path_to_file)

    def already_opened(self, file_path: str):
        return file_path in self.paths
