from pyabf import ABF
import file_handler as fh
from typing import List


class Logics:
    def __init__(self):
        self.abfs: list[ABF] = []

    def get_abfs(self) -> List[ABF]:
        return self.abfs

    def get_paths(self) -> List[str]:
        return [abf.abfFilePath for abf in self.abfs]

    def open_file_and_add_to_abf_infos(self, path_to_file):
        self.abfs.append(fh.open_abf(path_to_file))

    def open_abf(self, path_to_file):
        # if path to file is not empty, list is empty or if the path hasn't been already extracted, extract it
        if path_to_file and (not self.get_paths() or (path_to_file not in self.get_paths())):
            self.open_file_and_add_to_abf_infos(path_to_file)
        # else do nothing
