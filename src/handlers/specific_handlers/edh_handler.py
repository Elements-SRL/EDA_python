import os
from typing import List, Set
import numpy as np
import pyabf
from ordered_set import OrderedSet
from pyabf import ABF
from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup
from src.metadata.meta_data import MetaData
from src.handlers.specific_handlers import abf_handler


def extract_meta_data_from_edh(path_to_edh: str, metadata: MetaData):
    dir_path = os.path.dirname(os.path.realpath(path_to_edh))
    file_names = [file_path for file_path in os.listdir(dir_path) if file_path.endswith(".abf")]
    if _are_files_contiguous(file_names):
        # strategy for contiguous files
        # prefix length = prefix + _CHXXX_ = prefix+7
        prefix_length = file_names[0].find("_CH") + 7
        prefixes = {f[:prefix_length] for f in file_names}
        basic_data: OrderedSet[BasicData] = OrderedSet()
        dg: DataGroup | None = None
        for p in prefixes:
            batch_of_files = list(filter(lambda f_name: p in f_name, file_names))
            complete_batch_of_files = list(map(lambda f: dir_path + os.sep + f, batch_of_files))
            data: Set[BasicData] = set(_open_contiguous_abf(complete_batch_of_files))
            for d in data:
                print(d)
                basic_data.add(d)
            if dg is None:
                dg = _extract_data_group(path_to_files=complete_batch_of_files, path_to_edh=path_to_edh)
        dg.basic_data = basic_data
        metadata.add_data_group(dg)
    else:
        file_names = list(map(lambda file_name: dir_path + os.sep + file_name, file_names))
        _open_multiple_abf(path_to_files=file_names, metadata=metadata, path_to_edh=path_to_edh)


def _are_files_contiguous(file_names: List[str]) -> bool:
    for f in file_names:
        if not f.endswith("000.abf"):
            return True
    return False


def _open_multiple_abf(path_to_files: List[str], metadata: MetaData, path_to_edh: str):
    path_to_files.sort()
    basic_data = OrderedSet()
    for f in path_to_files:
        # abf_path = dir_path + os.sep + f
        data = abf_handler.extract_basic_data(path_to_file=f)
        for d in data:
            basic_data.add(d)
    # TODO extract number of channels from edh
    dg = abf_handler.extract_data_group(path_to_file=path_to_files.pop(), basic_data=basic_data)
    metadata.add_data_group(dg)


def _open_contiguous_abf(path_to_files_of_same_channels: List[str]) -> OrderedSet[BasicData]:
    # TODO SAFELY READ ONLY 9 CONTIGUOUS ABFS
    path_to_files_of_same_channels.sort()
    abfs = [pyabf.ABF(p) for p in path_to_files_of_same_channels]
    basic_data = _extract_data(abfs)
    return basic_data
    # metadata.add_data_group(_extract_data_group(abfs, basic_data))


def _extract_data_group(path_to_files: List[str], path_to_edh: str) -> DataGroup:
    with open(path_to_edh) as f:
        lines = [line.rstrip() for line in f]
    for line in lines:
        lowercase = line.lower()
        if lowercase.startswith("channels"):
            tokens = lowercase.split()
            n_channels = int(tokens[1])
            break
    print(path_to_files)
    abfs = [ABF(f) for f in path_to_files]
    x = abfs.pop(0).sweepX
    print(len(x))
    for abf in abfs:
        print(len(x))
        x = np.concatenate((x, abf.sweepX + x[-1:]), axis=None)
    abf.setSweep(0, 0)
    return DataGroup(x=x, sampling_rate=abf.sampleRate, channel_count=n_channels, measuring_unit=abf.sweepUnitsX,
                     sweep_label_x=abf.sweepLabelX, sweep_label_y=abf.sweepLabelY, sweep_label_c=abf.sweepLabelC,
                     sweep_count=abf.sweepCount,
                     )


def _extract_data(abfs: List[ABF]) -> OrderedSet[BasicData]:
    basic_data: OrderedSet[BasicData] = OrderedSet()
    for ch in range(abfs[0].channelCount):
        y = np.array([])
        for abf in abfs:
            abf.setSweep(channel=ch, sweepNumber=0)
            y = np.concatenate((y, abf.sweepY), axis=None)
        basic_data.add(BasicData(ch=ch, y=y, measuring_unit=abf.sweepUnitsY, sweep_number=0, file_path=abf.abfFilePath))
    return basic_data
