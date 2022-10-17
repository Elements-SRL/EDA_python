from typing import Iterable, Tuple

import numpy as np
from numpy import ndarray

from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup


def calc_data_group_hist(dg: DataGroup, n_bins: int = 10) -> DataGroup:
    # TODO calc hist only on y values?
    _, bins = dg.basic_data[0]
    # TODO problems of different bins in ch0-ch1
    bds = [_calc_bd_hist(bd, n_bins) for bd in dg.basic_data]
    return DataGroup()


# def calc_hist(bds: Iterable[BasicData], n_bins: int = 10) -> Tuple[ndarray, Iterable[float]]:
#     bds = [BasicData(ch=bd.ch) for bd]
#     return np.histogram(a, n_bins)


def _find_name(name: str) -> str:
    if name.endswith("hist"):
        return name + " 2"
    elif name[-1].isdigit():
        return name + str(int(name.split(" ").pop()) + 1)
    else:
        return name + "hist"


def _calc_bd_hist(bd: BasicData, n_bins: int = 10) -> BasicData:
    y, _ = np.histogram(bd.y, n_bins)
    name = _find_name(bd.name)
    return BasicData(ch=bd.ch, measuring_unit="-", sweep_number=bd.sweep_number, y=y, name=name, file_path=bd.filepath)
