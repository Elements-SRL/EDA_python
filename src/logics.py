import os
import csv

import numpy as np
import pyabf
from numpy import ndarray
from pyabf import ABF
from typing import List, Dict, Set
from os.path import exists


def contiguous_strategy(file_names: List[str]):
    prefix_length = file_names[0].find("_CH") + 7
    prefixes = {f[:prefix_length] for f in file_names}
    return prefixes


def get_abf_index(abf: ABF) -> str:
    channel_name_index = abf.abfID.find("_CH") + 1
    # 2 = CH
    index = abf.abfID.casefold()[channel_name_index + 2:-4]
    while index.startswith("0"):
        index = index[1:]
    return index


def get_channel_name(abf: ABF) -> str:
    # TODO channel should be a constant
    return "channel " + get_abf_index(abf)


def get_channel_name_abbreviation(abf: ABF) -> str:
    # TODO ch should be a constant
    return "ch" + get_channel_name(abf)[8:]


# if there are file contiguous some file must end with
def are_files_contiguous(file_names: List[str]) -> bool:
    for f in file_names:
        if not f.endswith("000.abf"):
            return True
    return False


def get_clean_sweeps(abf: ABF) -> {int: (List[ndarray], List[ndarray])}:
    expected_length = round(abf.sampleRate*abf.sweepIntervalSec)
    dict_to_return = {}
    for ch in range(abf.channelCount):
        sweepX = []
        sweepY = []
        for sweep in range(abf.sweepCount):
            abf.setSweep(sweep, ch)
            if len(abf.sweepX) > expected_length:
                # take 2 times the first values expected_length values
                sweepX.append(abf.sweepX[:expected_length])
                sweepX.append(abf.sweepX[:expected_length])
            elif len(abf.sweepX) == expected_length:
                sweepX.append(abf.sweepX)

            if len(abf.sweepY) > expected_length:
                sweepY.append(abf.sweepY[:expected_length])
                sweepY.append(abf.sweepY[expected_length+1:(expected_length*2)+1])
            elif len(abf.sweepY) == expected_length:
                sweepY.append(abf.sweepY)
        dict_to_return[ch] = (sweepX, sweepY)
    return dict_to_return


# TODO maybe get_abfs should be get_visible_abfs and get_visible_abfs would be deleted
class Logics:
    def __init__(self):
        self.abfs: List[ABF] = []
        # receiver could be a list of ABF, so this could change in future
        self.names_to_abfs: Dict[str, ABF] = {}
        self.hidden_channels: Set[str] = set()

    def get_abfs(self) -> List[ABF]:
        return self.abfs

    def get_visible_abfs(self) -> List[ABF]:
        dict_of_visible_abfs = {k: v for (k, v) in self.names_to_abfs.items() if k not in self.hidden_channels}
        return list(dict_of_visible_abfs.values())

    def get_paths(self) -> List[str]:
        return [abf.abfFilePath for abf in self.abfs]

    def clear(self):
        self.abfs.clear()
        self.names_to_abfs.clear()
        self.hidden_channels.clear()

    def add_to_hidden_channels(self, channel_to_hide: str):
        self.hidden_channels.add(channel_to_hide)

    def add_to_abs(self, abf):
        if abf.abfFilePath not in self.get_paths():
            self.abfs.append(abf)
            self.names_to_abfs[get_channel_name(abf)] = abf

    def open_abf_and_add_to_abfs(self, path_to_file):
        abf = pyabf.ABF(path_to_file)
        self.add_to_abs(abf)
        # print(abf.headerText)

    # TODO maybe change other stuff like range of time ecc
    def open_contiguous_abf(self, path_to_files_of_same_channels: List[str]):
        path_to_files_of_same_channels.sort()
        first_file = path_to_files_of_same_channels.pop(0)
        abf = pyabf.ABF(first_file)
        # merge useful information
        for p in path_to_files_of_same_channels:
            other_abf = pyabf.ABF(p)
            abf.sweepY = np.concatenate((abf.sweepY, other_abf.sweepY), axis=None)
            # time starts every time from zero
            abf.sweepX = np.concatenate((abf.sweepX, other_abf.sweepX + abf.sweepX[-1:]), axis=None)
            abf.sweepC = np.concatenate((abf.sweepC, other_abf.sweepC), axis=None)
            abf.data = [np.concatenate((d, od), axis=None) for d, od in zip(abf.data, other_abf.data)]
        self.add_to_abs(abf)

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
        file_names = [file_path for file_path in os.listdir(dir_path) if file_path.endswith(".abf")]
        if are_files_contiguous(file_names):
            # strategy for contiguous files
            # prefix length = prefix + _CHXXX_ = prefix+7
            prefix_length = file_names[0].find("_CH") + 7
            prefixes = {f[:prefix_length] for f in file_names}
            for p in prefixes:
                batch_of_files = list(filter(lambda f_name: p in f_name, file_names))
                complete_batch_of_files = list(map(lambda f: dir_path + os.sep + f, batch_of_files))
                self.open_contiguous_abf(complete_batch_of_files)
        else:
            file_names.sort()
            for f in file_names:
                abs_path = dir_path + os.sep + f
                self.open_abf_and_add_to_abfs(abs_path)

    # TODO does it work with multiple sweeps?
    def generate_header(self) -> List[str]:
        header = ["t[" + self.abfs[0].sweepUnitsX + "]"]
        for abf in self.get_abfs():
            header.append(get_channel_name_abbreviation(abf) + "[" + abf.sweepUnitsY + "]")
            header.append("vC" + get_abf_index(abf) + "[" + abf.sweepUnitsC + "]")
        return header

    # TODO does it work with multiple sweeps?
    # TODO transform data in exponential form
    def generate_data(self) -> List[List[int]]:
        # take the time from the first abf
        time = self.get_abfs()[0].sweepX
        data = [time]
        # get channel value and vC value
        for abf in self.get_abfs():
            # ch_i
            data.append(abf.sweepY)
            # vC_i
            data.append(abf.data[1])

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
        if channel_name not in self.hidden_channels:
            self.hidden_channels.add(channel_name)
        else:
            self.hidden_channels.remove(channel_name)

    def set_hidden_channel(self, channel: str, visible: bool):
        if visible and channel in self.hidden_channels:
            self.hidden_channels.remove(channel)
        if not visible and channel not in self.hidden_channels:
            self.hidden_channels.add(channel)
