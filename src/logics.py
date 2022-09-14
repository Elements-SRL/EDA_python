import os
import csv

import numpy as np
import pyabf
from pyabf import ABF
from typing import List, Dict, Set
from os.path import exists


def get_abf_index(abf: ABF) -> str:
    print(abf.abfID)
    channel_name_index = abf.abfID.find("_CH")+1
    # index = abf.abfID.casefold()[7:-4]
    # 2 = CH
    index = abf.abfID.casefold()[channel_name_index+2:-4]
    while index.startswith("0"):
        index = index[1:]
    return index


def get_channel_name(abf: ABF) -> str:
    # TODO channel should be a constant
    return "channel " + get_abf_index(abf)


def get_channel_name_abbreviation(abf: ABF) -> str:
    # TODO ch should be a constant
    return "ch" + get_channel_name(abf)[8:]


# TODO maybe get_abfs should be get_visible_abfs and get_visible_abfs would be deleted
class Logics:
    def __init__(self):
        self.abfs: List[ABF] = []
        # receiver could be a list of ABF, so this could change in future
        self.names_to_abfs: Dict[str, ABF] = {}
        self.hidden_channels: Set[str] = set()

    def get_abfs(self) -> List[ABF]:
        return self.abfs

    def get_visible_abfs(self):
        dict_of_visible_abfs = {k: v for (k, v) in self.names_to_abfs.items() if k not in self.hidden_channels}
        return list(dict_of_visible_abfs.values())

    def get_paths(self) -> List[str]:
        return [abf.abfFilePath for abf in self.abfs]

    def clear(self):
        self.abfs.clear()

    def add_to_hidden_channels(self, channel_to_hide: str):
        self.hidden_channels.add(channel_to_hide)

    def open_abf_and_add_to_abfs(self, path_to_file):
        # if list is empty or if the path hasn't been already extracted,
        abf = pyabf.ABF(path_to_file)
        # print(abf.headerText)
        if abf.abfFilePath not in self.get_paths():
            self.abfs.append(abf)
            self.names_to_abfs[get_channel_name(abf)] = abf

    def open(self, path_to_file):
        # if path to file is not empty extract it
        if not path_to_file or not exists(path_to_file):
            # TODO tell something to the user?
            return
        if path_to_file.endswith(".abf"):
            self.open_abf_and_add_to_abfs(path_to_file)
        elif path_to_file.endswith(".edh"):
            self.open_edh(path_to_file)
        # else do nothing

    # TODO read contiguous abfs
    def open_edh(self, path_to_file):
        dir_path = os.path.dirname(os.path.realpath(path_to_file))
        for root, dirs, files in os.walk(dir_path):
            files.sort()
            # TODO manage file composed of multiple files!!
            for file_name in files:
                if file_name.endswith(".abf"):
                    abs_path = dir_path + os.sep + file_name
                    self.open_abf_and_add_to_abfs(abs_path)

    # TODO does it work with multiple sweeps?
    def generate_header(self) -> List[str]:
        header = ["t[" + self.abfs[0].sweepUnitsX + "]"]
        for abf in self.get_abfs():
            header.append(get_channel_name_abbreviation(abf) + "[" + abf.sweepUnitsY + "]")
            header.append("vC" + get_abf_index(abf) + "[" + abf.sweepUnitsC + "]")
        return header

    # TODO does it work with multiple sweeps?
    def generate_data(self) -> List[List[int]]:
        # take the time from the first abf
        time = self.get_abfs()[0].sweepX
        data = [time]
        # get channel value and vC value
        for abf in self.get_abfs():
            # ch_i
            data.append(abf.sweepY)
            # vC_i
            data.append(abf.sweepC)

        # create matrix with all data
        arrays = np.array(data)

        # array with this form
        # [[t1,t2,..tn],
        #  [ch1_1, ch1_2.., ch1_n],
        #  [vC1_1, vC1_2,.., vC1_n],
        #  .
        #  .
        #  [chn_1, chn_2.., chn_n],
        #  [vCn_1, vCn_2,.., vCn_n]]

        formatted_data = []
        # for each value of time the get the corresponding data
        for i in range(len(time)):
            row = arrays[:, i]
            formatted_data.append(row)

        # now data is in the form
        # [[t1, ch1_1, vC1_1, .. chn_1, vCN_1],
        #  [t2, ch1_2, vC1_2, .. chn_2, vCN_2],
        #   .
        #   .
        #   [tn, ch1_n, vC1_n, .. chn_n, vCN_n]]
        return formatted_data

    def export(self, path_to_file):
        # TODO export only visible_abfs?
        if not self.get_abfs():
            # TODO tell something to the user?
            return
        #  TODO check if there is another file with the same name and change the name accordingly
        if os.path.exists(path_to_file):
            path_to_file = path_to_file
        # exporting csv files
        with open(path_to_file, 'w') as f:
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow(self.generate_header())
            data = self.generate_data()
            writer.writerows(data)

    def get_hidden_channels(self):
        return list(self.hidden_channels).sort()

    def toggle_visibility(self, channel_name: str):
        # if self.hidden_channels is None:
        #     self.hidden_channels = set(channel_name)
        #     return
        if channel_name not in self.hidden_channels:
            self.hidden_channels.add(channel_name)
        else:
            self.hidden_channels.remove(channel_name)

    def set_hidden_channel(self, channel: str, visible: bool):
        if visible and channel in self.hidden_channels:
            self.hidden_channels.remove(channel)
        if not visible and channel not in self.hidden_channels:
            self.hidden_channels.add(channel)
