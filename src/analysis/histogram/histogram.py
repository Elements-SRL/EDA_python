import numpy as np
from numpy import ndarray
from ordered_set import OrderedSet

from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup


def _name_strategy(name: str) -> str:
    if name.endswith("hist"):
        return name + " 1"
    if name[-1].isdigit():
        rev = name.split(" ")[::-1]
        if rev[1] == "hist":
            index = name.find(str(int(name.split(" ").pop()) + 1))
            return name[:index] + str(int(name.split(" ").pop()) + 1)
        else:
            return name + " hist"
    else:
        return name + " hist"


def calc_data_group_hist(dg: DataGroup, axis: int, n_bins: int = 10) -> DataGroup:
    # TODO calc hist only on y values?
    bins = _calc_bins(next(bd.y for bd in dg.basic_data if bd.axis == axis), n_bins)
    bds = OrderedSet([_calc_bd_hist(bd, n_bins) for bd in dg.basic_data if bd.axis == axis])
    return DataGroup(x=bins, name=_name_strategy(dg.name), basic_data=bds, channel_count=dg.channel_count,
                     sweep_count=dg.sweep_count, measuring_unit="bins avg", sweep_label_x="Bins", sweep_label_c="Count",
                     sweep_label_y="Count", sampling_rate=-1, type="hist")


def _calc_bins(y: ndarray, n_bins: int) -> ndarray:
    _, bins = np.histogram(y, n_bins)
    bin_values = []
    for i in range(len(bins) - 1):
        bin_values.append((bins[i] + bins[i + 1]) / 2)
    return np.array(bin_values)


def _calc_bd_hist(bd: BasicData, n_bins: int) -> BasicData:
    y, _ = np.histogram(bd.y, n_bins)
    name = _name_strategy(bd.name)
    return BasicData(ch=bd.ch, measuring_unit="Count", sweep_number=bd.sweep_number, y=y, name=name, file_path=bd.filepath,
                     axis=bd.axis)
