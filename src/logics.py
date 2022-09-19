import os
import csv

import numpy as np
import pyabf
from numpy import ndarray
from pyabf import ABF
from typing import List, Dict, Set
from os.path import exists


def get_abf_index(abf: ABF) -> str:
    channel_name_index = abf.abfID.find("_CH") + 1
    # 2 = CH
    index = abf.abfID.casefold()[channel_name_index + 2:-4]
    if index.startswith("0"):
        while index.startswith("0"):
            index = index[1:]
        return index
    else:
        return "-Nan"


def channel_name(abf: ABF) -> str:
    # TODO channel should be a constant
    return "channel " + get_abf_index(abf)


def channel_name_abbreviation(abf: ABF) -> str:
    # TODO ch should be a constant
    return "ch" + get_abf_index(abf)


# if there are file contiguous some file must end with
def are_files_contiguous(file_names: List[str]) -> bool:
    for f in file_names:
        if not f.endswith("000.abf"):
            return True
    return False


# TODO maybe refactor this?
# returns a dictionary with the channel as a key and a tuple of list(array) as value (one for the x and one for the y)
def get_clean_sweeps(abf: ABF) -> {int: (List[ndarray], List[ndarray])}:
    expected_length = round(abf.sampleRate * abf.sweepIntervalSec)
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
                sweepY.append(abf.sweepY[expected_length + 1:(expected_length * 2) + 1])
            elif len(abf.sweepY) == expected_length:
                sweepY.append(abf.sweepY)
        # TODO investigate why this slice is necessary
        dict_to_return[ch] = (sweepX[2:], sweepY[2:])
    return dict_to_return


class Logics:
    def __init__(self):
        self.abfs: List[ABF] = []
        self.names_to_abfs: Dict[str, ABF] = {}
        self.hidden_channels: Set[str] = set()
        self.hidden_sweeps: Set[int] = set()

    def get_abfs(self) -> List[ABF]:
        return self.abfs

    def get_visible_abfs(self) -> List[ABF]:
        dict_of_visible_abfs = {k: v for (k, v) in self.names_to_abfs.items() if k not in self.hidden_channels}
        return list(dict_of_visible_abfs.values())

    # TODO make some controls
    # TODO add return type
    def get_visible_sweeps(self) -> {int: (List[ndarray], List[ndarray])}:
        dict_of_sweeps = get_clean_sweeps(self.abfs[0])
        sweepX_ch0, sweepY_ch0 = dict_of_sweeps[0]
        sweepX_ch1, sweepY_ch1 = dict_of_sweeps[1]
        indexes = list(self.hidden_sweeps)
        indexes.sort(reverse=True)
        print(indexes)
        if len(indexes) > 0:
            for i in indexes:
                sweepX_ch0.pop(i)
                sweepY_ch0.pop(i)
                sweepX_ch1.pop(i)
                sweepY_ch1.pop(i)
            dict_to_return = {0: (sweepX_ch0, sweepY_ch0), 1: (sweepX_ch1, sweepY_ch1)}
            return dict_to_return
        else:
            return dict_of_sweeps

    def get_paths(self) -> List[str]:
        return [abf.abfFilePath for abf in self.abfs]

    def clear(self):
        self.abfs.clear()
        self.names_to_abfs.clear()
        self.hidden_channels.clear()
        self.hidden_sweeps.clear()

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

    def open_abf_and_add_to_abfs(self, path_to_file):
        abf = pyabf.ABF(path_to_file)
        self.add_to_abs(abf)
        # print(abf.headerText)

    def add_to_abs(self, abf):
        if abf.abfFilePath not in self.get_paths():
            self.abfs.append(abf)
            self.names_to_abfs[channel_name(abf)] = abf

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

    def export(self, path_to_file):
        # TODO export only visible_abfs?
        if not self.get_abfs():
            # TODO tell something to the user?
            return
        # exporting csv files
        with open(path_to_file, 'w') as f:
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow(self.generate_header())
            data = self.generate_data()
            writer.writerows(data)

    # TODO does it work with multiple sweeps?
    def generate_header(self) -> List[str]:
        header = ["t[" + self.abfs[0].sweepUnitsX + "]"]
        for abf in self.get_abfs():
            header.append(channel_name_abbreviation(abf) + "[" + abf.sweepUnitsY + "]")
            header.append("vC" + get_abf_index(abf) + "[" + abf.sweepUnitsC + "]")
        return header

    def generate_data(self) -> List[List[float]]:
        first_abf = self.get_abfs()[0]
        if first_abf.sweepCount > 1:
            return self.format_to_csv(self.generate_multi_sweep_data(first_abf))
        # take the time from the first abf
        time = self.get_abfs()[0].sweepX
        data = [time]
        # get channel value and vC value
        for abf in self.get_abfs():
            # ch_i
            data.append(abf.sweepY)
            # vC_i
            data.append(abf.data[1])
        return self.format_to_csv(data)

    # TODO add last fields as in the notes
    @staticmethod
    def generate_multi_sweep_data(abf) -> List[ndarray]:
        dict_of_sweeps = get_clean_sweeps(abf)
        sweepX_ch0, sweepY_ch0 = dict_of_sweeps[0]
        sweepX_ch1, sweepY_ch1 = dict_of_sweeps[1]
        time = np.tile(sweepX_ch0.pop(0), abf.sweepCount + 2)
        return [time, np.hstack(sweepY_ch0), np.hstack(sweepY_ch1)]

    @staticmethod
    def format_to_csv(data: List[List[float]] | List[ndarray]):
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
        for i in range(len(data[0])):
            row = arrays[:, i]
            formatted_data.append(row)

        # now data is in the form
        # [[t1, ch1_1, vC1_1, .. chn_1, vCN_1],
        #  [t2, ch1_2, vC1_2, .. chn_2, vCN_2],
        #   .
        #   .
        #   [tn, ch1_n, vC1_n, .. chn_n, vCN_n]]
        return formatted_data

    def set_channel_visibility(self, channel: str, visible: bool):
        if visible and channel in self.hidden_channels:
            self.hidden_channels.remove(channel)
        if not visible:
            self.hidden_channels.add(channel)

    def set_sweep_visibility(self, sweep: int, visible: bool):
        if visible and sweep in self.hidden_sweeps:
            self.hidden_sweeps.remove(sweep)
        if not visible:
            self.hidden_sweeps.add(sweep)
