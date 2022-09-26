from os.path import exists
from src.data_classes.meta_data import MetaData
import handlers.abf_handler as abf_handler


class Logics2:
    def __init__(self):
        self.metadata = MetaData()

    def open(self, path_to_file):
        # if path to file is not empty extract it
        if not path_to_file or not exists(path_to_file):
            # TODO tell something to the user?
            return
        abf_handler.extract_meta_data_from_abf(path_to_file, self.metadata)
        # else do nothing

    def is_all_data_hidden(self):
        return True not in {v.visible for v in self.metadata.data}

    def get_x(self):
        self.metadata.get_x()

    def clear(self):
        self.metadata.data.clear()
        self.metadata.common_data = None
