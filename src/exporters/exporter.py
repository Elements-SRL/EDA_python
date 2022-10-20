import csv
from typing import List

from numpy import ndarray
import numpy as np
from src.metadata.meta_data import MetaData


def export(path_to_file: str, metadata: MetaData):
    # exporting csv files
    with open(path_to_file, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(_generate_header(metadata=metadata))
        writer.writerows(_generate_data_in_columnar_form(metadata=metadata))


def _generate_header(metadata: MetaData) -> List[str]:
    # header starts with measuring unit of x values
    header = [metadata.selected_data_group.measuring_unit]
    for ch in range(metadata.selected_data_group.channel_count * 2):
        if metadata.selected_data_group.sweep_count > 1:
            measuring_unit = {d.measuring_unit for d in metadata.selected_data_group.basic_data if d.ch == ch}
        else:
            measuring_unit = [d.measuring_unit for d in metadata.selected_data_group.basic_data if d.ch == ch]
        header.extend(measuring_unit)
    return header


def _generate_data_in_columnar_form(metadata: MetaData) -> ndarray:
    different_file_paths = {d.filepath for d in metadata.selected_data_group.basic_data}
    if metadata.selected_data_group.sweep_count > 1:
        rows_data = np.tile(metadata.get_x(), metadata.selected_data_group.sweep_count)
    else:
        rows_data = metadata.get_x()
    for ch in range(metadata.selected_data_group.channel_count * 2):
        for file_path in different_file_paths:
            data_with_same_file_path = [d for d in metadata.selected_data_group.basic_data if d.filepath == file_path]
            data_with_same_channel = [d for d in data_with_same_file_path if d.ch == ch]
            sorted_data = sorted(data_with_same_channel, key=lambda data: data.sweep_number)
            if len(sorted_data) > 0:
                y = sorted_data.pop(0).y
                for d in sorted_data:
                    if metadata.selected_data_group.sweep_count > 1:
                        y = np.concatenate((y, d.y), axis=None)
                    else:
                        y = np.vstack((y, d.y))
                rows_data = np.vstack((rows_data, y))
    return np.transpose(rows_data)
