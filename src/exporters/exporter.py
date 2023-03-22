import csv
from typing import List, Iterable, Tuple

from numpy import ndarray
import numpy as np

from src.analysis.fitting.FittingParams import FittingParams
from src.metadata.meta_data import MetaData
from src.constants.strings import *


def export(path_to_file: str, metadata: MetaData):
    # exporting csv files
    with open(path_to_file, 'w', newline="") as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(_generate_header(metadata=metadata))
        writer.writerows(_generate_data_in_columnar_form(metadata=metadata))


def _generate_header(metadata: MetaData) -> List[str]:
    return [metadata.selected_data_group.measuring_unit] + [bd.measuring_unit for bd in
                                                            metadata.selected_data_group.basic_data if
                                                            bd.sweep_number == 0]


def _generate_data_in_columnar_form(metadata: MetaData) -> ndarray:
    different_file_paths = {d.filepath for d in metadata.selected_data_group.basic_data}
    rows_data = metadata.get_x() if metadata.selected_data_group.sweep_count == 1 else np.tile(metadata.get_x(),
                                                                                               metadata.selected_data_group.sweep_count)
    for ch in {bd.ch for bd in metadata.selected_data_group.basic_data}:
        for file_path in different_file_paths:
            same_file_path_and_channel = [d for d in metadata.selected_data_group.basic_data if
                                          d.filepath == file_path and d.ch == ch]
            sorted_data = sorted(same_file_path_and_channel, key=lambda data: data.sweep_number)
            if len(sorted_data) > 0:
                # flatten list of y data
                y = [item for sublist in [d.y for d in sorted_data] for item in sublist]
                rows_data = np.vstack((rows_data, y))
    return np.transpose(rows_data)


def export_fitting_params_to_csv(path_to_file: str, equation: str, fitting_params: Iterable[FittingParams]):
    with open(path_to_file, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(["Equation", equation])
        for r in [[["ch", f.ch], ["measuring unit", f.measuring_unit], *[[p[0], p[1]] for p in f.popt]] for f in
                  fitting_params]:
            writer.writerows(r)


def export_events_to_csv(path_to_file: str, events: List[Tuple[float, int, int, int]], measuring_unit: str):
    with open(path_to_file, 'w', newline="") as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow([AMPLITUDE_LABEL + " " + measuring_unit, DURATION_LABEL, START_OF_EVENT_LABEL, END_OF_EVENT_LABEL])
        writer.writerows([[e[0], e[1], e[2], e[3]] for e in events])
