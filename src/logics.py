import math
from os.path import exists
from typing import Iterable

import numpy as np
from numpy import ndarray
from ordered_set import OrderedSet

from src.analysis.fitting import fitting
from src.analysis.histogram import histogram
from src.metadata.data_classes.data_group import DataGroup
from src.metadata.data_classes import data_group
from src.exporters import exporter
from src.analysis.filters import filter_handler
from src.analysis.filters.filter_arguments import FilterArguments
from src.file_handlers import file_handler
from src.metadata.data_classes.basic_data import BasicData
from src.metadata.meta_data import MetaData
from src.analysis.spectral_analysis import spectral_analysis as sa


def _create_fit_basic_data(x: ndarray, bd: BasicData, func) -> BasicData:
    y, _ = func(x, bd.y)
    return BasicData(ch=bd.ch, y=y, sweep_number=bd.sweep_number, measuring_unit=bd.measuring_unit,
                     file_path=bd.filepath, name=bd.name + " fit", axis=bd.axis)


class Logics:
    def __init__(self):
        self.metadata: MetaData = MetaData()

    def open(self, path_to_file):
        # if path to file is not empty extract it
        if not path_to_file or not exists(path_to_file):
            # TODO tell something to the user?
            return
        file_handler.extract_data(path_to_file, self.metadata)
        # else do nothing

    def is_all_data_hidden(self):
        return True if self.metadata.selected_data_group is None \
            else True not in {v.visible for v in self.metadata.selected_data_group.basic_data}

    def clear(self):
        self.metadata.clear()

    def export(self, path_to_file: str):
        if not self.metadata.is_empty():
            return exporter.export(path_to_file=path_to_file, metadata=self.metadata)

    def filter_preview(self, filter_args: FilterArguments):
        return filter_handler.calc_filter(filter_args)

    def filter_selected_data_group(self, filter_args: FilterArguments):
        updated_data = [BasicData(ch=d.ch,
                                  y=filter_handler.filter_signal(filter_args, d.y),
                                  sweep_number=d.sweep_number,
                                  measuring_unit=d.measuring_unit,
                                  file_path=d.filepath,
                                  name=d.name,
                                  axis=d.axis,
                                  ) for d in self.metadata.selected_data_group.basic_data]
        sdg = self.metadata.selected_data_group
        dg = data_group.make_copy(sdg, self.metadata.get_and_increment_id())
        dg.basic_data = updated_data
        sdg.data_groups.add(dg)
        dg.name = str(dg.id) + " " + dg.name.split(" ")[1][:4] + " " + filter_args.filter_type[:4] + \
                  " ord " + str(filter_args.order) + " " + filter_args.b_type
        self.metadata.selected_data_group = dg

    def select_data_group(self, name):
        dg = self._recursive_search(name, data_groups=self.metadata.data_groups)
        self.metadata.selected_data_group = dg

    def _recursive_search(self, name: str, data_groups: Iterable[DataGroup]) -> DataGroup:
        for dg in data_groups:
            if dg.name == name:
                return dg
            if len(dg.data_groups) > 0:
                found_dg = self._recursive_search(name, dg.data_groups)
                if found_dg is not None:
                    return found_dg

    def spectral_analysis(self):
        bd = self.metadata.selected_data_group.basic_data
        bd_ch0 = [self._create_spectral_analysis_basic_data(d, 0) for d in bd if d.ch == 0]
        bd_ch1 = [self._create_spectral_analysis_basic_data(d, 1) for d in bd if d.ch == 1]
        bd = OrderedSet(bd_ch0 + bd_ch1)
        dg = self._create_spectral_analysis_data_group(self.metadata.selected_data_group, bd)
        self.metadata.selected_data_group.data_groups.add(dg)
        self.metadata.selected_data_group = dg

    def hist(self, n_bins: int = -1):
        if n_bins == -1:
            n_bins = math.floor(math.sqrt(len(self.metadata.get_x())))
        # TODO Tell something to the user about the creation of 2 datagroups
        axis = sorted(list({bd.axis for bd in self.metadata.selected_data_group.basic_data}))
        dgs = [histogram.calc_data_group_hist(dg=self.metadata.selected_data_group, axis=ax, n_bins=n_bins) for ax in axis]
        for dg in dgs:
            self._common_hist_ops(dg)
            self.metadata.selected_data_group.data_groups.add(dg)
        self.metadata.selected_data_group = dgs[0]

    def _common_hist_ops(self, dg: DataGroup):
        dg.id = self.metadata.get_and_increment_id()
        dg.name = str(dg.id) + dg.name[dg.name.find(" "):]

    def _create_spectral_analysis_basic_data(self, d: BasicData, ch: int) -> BasicData:
        fs = self.metadata.selected_data_group.sampling_rate
        x, Pxx = sa.spectral_analysis(x=d.y, fs=fs)
        m_unit = '[' + d.measuring_unit + '²/Hz]'
        name = d.name + " PSD"
        return BasicData(ch=ch, y=Pxx, sweep_number=d.sweep_number, measuring_unit=m_unit, file_path=d.filepath,
                         name=name, axis=d.axis)

    def _create_spectral_analysis_data_group(self, odg: DataGroup, bd: OrderedSet[BasicData]) -> DataGroup:
        f, _ = sa.spectral_analysis(x=self.metadata.selected_data_group.basic_data[0].y, fs=odg.sampling_rate)
        l_0 = bd[0].measuring_unit
        l_1 = bd[len(bd) - 1].measuring_unit
        x_label, y_label, c_label = "Frequency [Hz]", l_0, l_1
        new_id = self.metadata.get_and_increment_id()
        name = str(new_id) + " " + odg.name.split(" ")[1][:4] + " PSD"
        return DataGroup(x=f, data_groups=set(), channel_count=odg.channel_count,
                         sweep_count=odg.sweep_count, sweep_label_x=x_label, sweep_label_y=y_label,
                         sweep_label_c=c_label, basic_data=bd, id=new_id,
                         measuring_unit='Hz', name=name, sampling_rate=odg.sampling_rate, type="psd")

    def create_new_range(self, x_min: float, x_max: float):
        dg = data_group.make_copy(self.metadata.selected_data_group, self.metadata.get_and_increment_id())
        dg.name = str(dg.id) + " " + self.metadata.selected_data_group.name.split(" ")[1][:4]
        idx_of_min, idx_of_max = (np.abs(dg.x - x_min)).argmin(), (np.abs(dg.x - x_max)).argmin()
        new_bd = [BasicData(ch=bd.ch, y=bd.y[idx_of_min: idx_of_max], sweep_number=bd.sweep_number,
                            measuring_unit=bd.measuring_unit, file_path=bd.filepath, name=bd.name, axis=bd.axis)
                  for bd in dg.basic_data]
        dg.x = dg.x[idx_of_min:idx_of_max]
        dg.basic_data = OrderedSet(new_bd)
        self.metadata.selected_data_group.data_groups.add(dg)
        self.metadata.selected_data_group = dg

    def fit(self, function_name: str):
        if function_name.startswith("linear"):
            self._perform_fit(fitting.linear_fitting)
        elif function_name.startswith("quadratic"):
            self._perform_fit(fitting.quadratic_fitting)
        elif function_name.startswith("exponential"):
            self._perform_fit(fitting.exponential_fitting)
        elif function_name.startswith("power_law"):
            self._perform_fit(fitting.power_law_fitting)
        elif function_name.startswith("gaussian"):
            self._perform_fit(fitting.gaussian_fitting)
        else:
            print(function_name)

    def _perform_fit(self, func):
        dg = data_group.make_copy(self.metadata.selected_data_group, self.metadata.get_and_increment_id())
        new_bd = [BasicData(ch=bd.ch, y=bd.y, axis=bd.axis, file_path=bd.filepath, measuring_unit=bd.measuring_unit,
                            name=bd.name) for bd in dg.basic_data]
        oset = OrderedSet(new_bd)
        fit_bd = [_create_fit_basic_data(dg.x, bd, func) for bd in dg.basic_data]
        dg.type = "fitting"
        dg.name = str(dg.id) + " " + self.metadata.selected_data_group.name.split(" ")[1][:4] + " fit"
        for bd in fit_bd:
            oset.add(bd)
        dg.basic_data = oset
        self.metadata.selected_data_group.data_groups.add(dg)
        self.metadata.selected_data_group = dg
