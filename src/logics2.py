from os.path import exists

from src import file_handler, exporter
from src.data_classes.meta_data import MetaData


class Logics2:
    def __init__(self):
        self.metadata = MetaData()

    def open(self, path_to_file):
        # if path to file is not empty extract it
        if not path_to_file or not exists(path_to_file):
            # TODO tell something to the user?
            return
        file_handler.extract_data(path_to_file, self.metadata)
        # else do nothing

    def is_all_data_hidden(self):
        return True not in {v.visible for v in self.metadata.data}

    def clear(self):
        self.metadata.clear()

    def export(self, path_to_file: str):
        if self.metadata.is_empty():
            return
        exporter.export(path_to_file=path_to_file, metadata=self.metadata)
