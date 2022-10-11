from os.path import exists
from typing import Iterable

from src.metadata.data_classes.data_group import DataGroup
from src.metadata.data_classes import data_group
from src.exporters import exporter
from src.filters import filter_handler
from src.filters.filter_arguments import FilterArguments
from src.file_handlers import file_handler
from src.metadata.data_classes.basic_data import BasicData
from src.metadata.meta_data import MetaData


class Logics:
    def __init__(self):
        self.metadata: MetaData = MetaData()

    def open(self, path_to_file):
        # if path to file is not empty extract it
        if not path_to_file or not exists(path_to_file):
            # TODO tell something to the user?
            return
        file_handler.extract_data(path_to_file, self.metadata)
        # else do nothing

    def is_all_data_hidden(self):
        return True if self.metadata.selected_data_group is None \
            else True not in {v.visible for v in self.metadata.selected_data_group.basic_data}

    def clear(self):
        self.metadata.clear()

    def export(self, path_to_file: str):
        if not self.metadata.is_empty():
            return exporter.export(path_to_file=path_to_file, metadata=self.metadata)

    def filter_preview(self, filter_args: FilterArguments):
        return filter_handler.calc_filter(filter_args)

    def filter_selected_data_group(self, filter_args: FilterArguments):
        # TODO set new name with transformation
        updated_data = [BasicData(ch=d.ch,
                                  y=filter_handler.filter_signal(filter_args, d.y),
                                  sweep_number=d.sweep_number,
                                  measuring_unit=d.measuring_unit,
                                  file_path=d.filepath,
                                  name=d.name
                                  ) for d in self.metadata.selected_data_group.basic_data]
        sdg = self.metadata.selected_data_group
        dg = data_group.make_copy(sdg, self.metadata.get_and_increment_id())
        dg.basic_data = updated_data
        sdg.data_groups.add(dg)
        dg.name = str(dg.id) + " " + dg.name.split(" ")[1][:4] + " " + filter_args.filter_type[:4] + \
                  " ord " + str(filter_args.order) + " " + filter_args.b_type
        self.metadata.selected_data_group = dg

    def select_data_group(self, name):
        dg = self._recursive_search(name, data_groups=self.metadata.data_groups)
        self.metadata.selected_data_group = dg

    def _recursive_search(self, name: str, data_groups: Iterable[DataGroup]) -> DataGroup:
        for dg in data_groups:
            if dg.name == name:
                return dg
            if len(dg.data_groups) > 0:
                return self._recursive_search(name, dg.data_groups)
