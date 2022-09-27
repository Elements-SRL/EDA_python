import os
from typing import List

import numpy as np
import pyabf
from pyabf import ABF

from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import CommonData
from src.data_classes.meta_data import MetaData
# import abf_handler
from src.handlers import abf_handler


def _are_files_contiguous(file_names: List[str]) -> bool:
    for f in file_names:
        if not f.endswith("000.abf"):
            return True
    return False


def extract_meta_data_from_edh(path_to_file: str, metadata: MetaData):
    dir_path = os.path.dirname(os.path.realpath(path_to_file))
    file_names = [file_path for file_path in os.listdir(dir_path) if file_path.endswith(".abf")]
    if _are_files_contiguous(file_names):
        # strategy for contiguous files
        # prefix length = prefix + _CHXXX_ = prefix+7
        prefix_length = file_names[0].find("_CH") + 7
        prefixes = {f[:prefix_length] for f in file_names}
        for p in prefixes:
            batch_of_files = list(filter(lambda f_name: p in f_name, file_names))
            complete_batch_of_files = list(map(lambda f: dir_path + os.sep + f, batch_of_files))
            open_contiguous_abf(metadata, complete_batch_of_files)
    else:
        open_multiple_abf(path_to_files=file_names, dir_path=dir_path, metadata=metadata)


def open_multiple_abf(path_to_files: List[str], dir_path: str, metadata: MetaData):
    path_to_files.sort()
    for f in path_to_files:
        abs_path = dir_path + os.sep + f
        abf_handler.extract_meta_data_from_abf(metadata=metadata, path_to_file=abs_path)


def open_contiguous_abf(metadata: MetaData, path_to_files_of_same_channels: List[str]):
    path_to_files_of_same_channels.sort()
    first_file = path_to_files_of_same_channels.pop(0)
    abf = pyabf.ABF(first_file)
    # merge useful information
    for p in path_to_files_of_same_channels:
        other_abf = pyabf.ABF(p)
        abf.sweepY = np.concatenate((abf.sweepY, other_abf.sweepY), axis=None)
        # time starts every time from zero
        abf.sweepX = np.concatenate((abf.sweepX, other_abf.sweepX + abf.sweepX[-1:]), axis=None)
        # abf.sweepC = np.concatenate((abf.sweepC, other_abf.sweepC), axis=None)
        abf.data = [np.concatenate((d, od), axis=None) for d, od in zip(abf.data, other_abf.data)]
    if metadata.is_empty():
        metadata.common_data = CommonData(x=abf.sweepX, sampling_rate=abf.sampleRate, channel_count=abf.channelCount)
    metadata.add_data(BasicData(ch=0, y=abf.sweepY))
    metadata.add_data(BasicData(ch=1, y=abf.data[1]))

