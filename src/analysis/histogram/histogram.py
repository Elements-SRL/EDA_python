from typing import Iterable, Tuple, List

import numpy as np
from numpy import ndarray
from ordered_set import OrderedSet

from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup


def _name_strategy(name: str) -> str:
    if name.endswith("hist"):
        return name + " 1"
    if name[-1].isdigit():
        return name + str(int(name.split(" ").pop()) + 1)
    else:
        return name + "hist"


def calc_data_group_hist(dg: DataGroup, n_bins: int = 10) -> DataGroup:
    # TODO calc hist only on y values?
    bin_0 = _calc_bins(next(bd.y for bd in dg.basic_data if bd.axis == 0), n_bins)
    bin_1 = _calc_bins(next(bd.y for bd in dg.basic_data if bd.axis == 1), n_bins)
    bds = OrderedSet([_calc_bd_hist(bd, n_bins) for bd in dg.basic_data])
    return DataGroup(x=[bin_0, bin_1], name=_name_strategy(dg.name), basic_data=bds, channel_count=dg.channel_count,
                     sweep_count=dg.sweep_count, measuring_unit="-", sweep_label_x="", sweep_label_c="",
                     sweep_label_y="", sampling_rate=-1)


def _find_name(name: str) -> str:
    if name.endswith("hist"):
        return name + " 2"
    elif name[-1].isdigit():
        return name + str(int(name.split(" ").pop()) + 1)
    else:
        return name + "hist"


def _calc_bins(y: ndarray, n_bins: int) -> ndarray:
    _, bins = np.histogram(y, n_bins)
    bin_values = []
    for i in range(len(bins) - 1):
        bin_values.append((bins[i] + bins[i + 1]) / 2)
    return np.array(bin_values)


def _calc_bd_hist(bd: BasicData, n_bins: int) -> BasicData:
    y, _ = np.histogram(bd.y, n_bins)
    name = _find_name(bd.name)
    return BasicData(ch=bd.ch, measuring_unit="-", sweep_number=bd.sweep_number, y=y, name=name, file_path=bd.filepath,
                     axis=bd.axis)
