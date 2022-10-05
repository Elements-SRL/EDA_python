from typing import Set, List, Tuple
from ordered_set import OrderedSet
from numpy import ndarray

from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup


class MetaData:

    def __init__(self):
        self.selected_data_group: DataGroup | None = None
        self.data_groups: OrderedSet[DataGroup] = OrderedSet()
        self.paths: Set[str] = set()
        self.currentId: int = 0

    def clear(self):
        self.data_groups.clear()
        self.paths.clear()
        self.currentId = 0

    def get_x(self) -> ndarray:
        return self.selected_data_group.x

    def get_channel_y(self, channel: int) -> List[ndarray]:
        return [d.y for d in self.selected_data_group.basic_data if d.ch == channel]

    def get_all_y(self) -> List[Tuple[int, List[ndarray]]]:
        d = {ch: self.get_channel_y(ch) for ch in range(self.common_data.channel_count)}
        return list(zip(d.keys(), d.values()))

    # def add_data(self, basic_data: BasicData):
    #     if basic_data not in self.data:
    #         self.data.add(basic_data)
    #         basic_data.name = str(self.currentId)
    #         self.currentId += 1

    def get_visible_data(self) -> List[BasicData]:
        return [d for d in self.selected_data_group.basic_data if d.visible]

    def is_empty(self):
        return len(self.selected_data_group.basic_data) == 0 or self.selected_data_group is None

    def set_visibility(self, name: str, visibility: bool):
        for d in self.selected_data_group.basic_data:
            if d.name == name:
                d.visible = visibility

    def add_path(self, path_to_file):
        self.paths.add(path_to_file)

    def already_opened(self, file_path: str):
        return file_path in self.paths

    # TODO check if it is already inserted
    def add_data_group(self, dg: DataGroup):
        """add the data group if not already present and sets it as the selected one"""
        if dg in self.data_groups:
            return
        if dg.id == -1:
            dg.id = self.currentId
            self.currentId += 1
            self.selected_data_group = dg
            self.data_groups.add(dg)
