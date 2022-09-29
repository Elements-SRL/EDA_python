import os
from typing import List
import numpy as np
import pyabf
from pyabf import ABF
from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import CommonData, SweepType
from src.data_classes.meta_data import MetaData
from src.handlers import abf_handler


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
            _open_contiguous_abf(metadata, complete_batch_of_files)
    else:
        _open_multiple_abf(path_to_files=file_names, dir_path=dir_path, metadata=metadata)


def _are_files_contiguous(file_names: List[str]) -> bool:
    for f in file_names:
        if not f.endswith("000.abf"):
            return True
    return False


def _open_multiple_abf(path_to_files: List[str], dir_path: str, metadata: MetaData):
    path_to_files.sort()
    for f in path_to_files:
        abs_path = dir_path + os.sep + f
        abf_handler.extract_meta_data_from_abf(metadata=metadata, path_to_file=abs_path)


def _open_contiguous_abf(metadata: MetaData, path_to_files_of_same_channels: List[str]):
    # TODO SAFELY READ ONLY 9 CONTIGUOUS ABFS
    path_to_files_of_same_channels.sort()
    abfs = [pyabf.ABF(p) for p in path_to_files_of_same_channels]
    basic_data = _extract_data(abfs)
    if metadata.is_empty():
        metadata.common_data = _extract_common_data(abfs)
    for data in basic_data:
        metadata.add_data(data)


def _extract_common_data(abfs: List[ABF]) -> CommonData:
    x = abfs.pop(0).sweepX
    for abf in abfs:
        x = np.concatenate((x, abf.sweepX + x[-1:]), axis=None)
    abf.setSweep(0, 0)
    return CommonData(x=x, sampling_rate=abf.sampleRate, channel_count=abf.channelCount,
                      sweep_type=SweepType.episodic, measuring_unit=abf.sweepUnitsX,
                      sweep_label_x=abf.sweepLabelX, sweep_label_y=abf.sweepLabelY,
                      sweep_label_c=abf.sweepLabelC,
                      )


def _extract_data(abfs: List[ABF]) -> List[BasicData]:
    basic_data: List[BasicData] = list()
    for ch in range(abfs[0].channelCount):
        y = np.array([])
        for abf in abfs:
            abf.setSweep(channel=ch, sweepNumber=0)
            y = np.concatenate((y, abf.sweepY), axis=None)
        basic_data.append(BasicData(ch=ch, y=y, measuring_unit=abf.sweepUnitsY, sweep_number=0, file_path=abf.abfFilePath))
    return basic_data
