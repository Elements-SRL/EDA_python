import os
import csv
import pyabf
from pyabf import ABF
from typing import List
from os.path import exists


def get_abf_index(abf: ABF) -> int:
    index = abf.abfID.casefold()[7:-4]
    while index.startswith("0"):
        index = index[1:]


def get_channel_name(abf: ABF) -> str:
    # TODO channel should be a constant
    return "channel " + str(get_abf_index(abf))


def get_channel_name_abbreviation(abf: ABF) -> str:
    ch_name = get_channel_name(abf)
    return ch_name[:2]+ch_name[8:]


class Logics:
    def __init__(self):
        self.abfs: list[ABF] = []

    def get_abfs(self) -> List[ABF]:
        return self.abfs

    def get_paths(self) -> List[str]:
        return [abf.abfFilePath for abf in self.abfs]

    def open_abf_and_add_to_abfs(self, path_to_file):
        # if list is empty or if the path hasn't been already extracted,
        abf = pyabf.ABF(path_to_file)
        # print(abf.headerText)
        if abf.abfFilePath not in self.get_paths():
            self.abfs.append(abf)

    def open(self, path_to_file):
        # if path to file is not empty extract it
        if not path_to_file or not exists(path_to_file):
            return
        if path_to_file.endswith(".abf"):
            self.open_abf_and_add_to_abfs(path_to_file)
        elif path_to_file.endswith(".edh"):
            self.open_edh(path_to_file)
        # else do nothing

    def open_edh(self, path_to_file):
        dir_path = os.path.dirname(os.path.realpath(path_to_file))
        for root, dirs, files in os.walk(dir_path):
            for file_name in files:
                if file_name.endswith(".abf"):
                    abs_path = dir_path + os.sep + file_name
                    self.open_abf_and_add_to_abfs(abs_path)

    def generate_header(self) -> List[str] | None:
        if len(self.get_abfs()) == 0:
            return
        header = ["t[" + self.abfs[0].sweepUnitsX + "]"]
        for abf in self.get_abfs():
            header.append("[" + abf.sweepUnitsY + "]")
            header.append()
        print(header)
        return

    # def export(self, path_to_file):
    #     with open('path/to/csv_file', 'w') as f:
    #
    #         # create the csv writer
    #         writer = csv.writer(f)
    #
    #         # write a row to the csv file
    #         writer.writerow(row)
