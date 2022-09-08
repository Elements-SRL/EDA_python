import pyabf
from pyabf import ABF
from typing import List
from os.path import exists


class Logics:
    def __init__(self):
        self.abfs: list[ABF] = []

    def get_abfs(self) -> List[ABF]:
        return self.abfs

    def get_paths(self) -> List[str]:
        return [abf.abfFilePath for abf in self.abfs]

    def open_file_and_add_to_abfs(self, path_to_file):
        # if list is empty or if the path hasn't been already extracted,
        abf = pyabf.ABF(path_to_file)
        if abf.abfFilePath not in self.get_paths():
            self.abfs.append(abf)

    def open_abf(self, path_to_file):
        # if path to file is not empty extract it
        if path_to_file and exists(path_to_file):
            if path_to_file.endswith(".abf"):
                self.open_file_and_add_to_abfs(path_to_file)
        # else do nothing
