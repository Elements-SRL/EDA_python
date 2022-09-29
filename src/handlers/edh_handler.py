import os
from typing import List

import numpy as np
import pyabf
from pyabf import ABF

from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import CommonData, SweepType
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
    # TODO SAFELY READ ONLY 9 CONTIGUOUS ABFS
    path_to_files_of_same_channels.sort()
    abfs = [pyabf.ABF(p) for p in path_to_files_of_same_channels]
    first_abf = abfs[0]
    x = first_abf.sweepX
    first_abf.setSweep(channel=0, sweepNumber=0)
    y0 = first_abf.sweepY
    first_abf.setSweep(channel=1, sweepNumber=0)
    y1 = first_abf.sweepY
    i = 0
    for other in abfs:
        print(i)
        i += 1
        other.setSweep(channel=0, sweepNumber=0)
        print("canale 0")
        print(other.sweepUnitsY)
        x = np.concatenate((x, other.sweepX + x[-1:]), axis=None)
        y0 = np.concatenate((y0, other.sweepY), axis=None)
        other.setSweep(channel=1, sweepNumber=0)
        print("canale 1")
        print(other.sweepUnitsY)
        y1 = np.concatenate((y1, other.sweepY), axis=None)
    if metadata.is_empty():
        metadata.common_data = CommonData(x=x,
                                          sampling_rate=first_abf.sampleRate,
                                          channel_count=first_abf.channelCount,
                                          sweep_type=SweepType.episodic,
                                          measuring_unit=first_abf.sweepUnitsX)
    first_abf.setSweep(channel=0, sweepNumber=0)
    metadata.add_data(BasicData(ch=0, y=y0, measuring_unit=first_abf.sweepUnitsY, sweep_number=0))
    first_abf.setSweep(channel=1, sweepNumber=0)
    metadata.add_data(BasicData(ch=1, y=y1, measuring_unit=first_abf.sweepUnitsY, sweep_number=0))

# TODO fare un metodo che dati n abf e un canale li sputi fuori una y con tutti gli abf concatenati?
