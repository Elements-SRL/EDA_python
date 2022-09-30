import csv
from typing import List

from numpy import ndarray
import numpy as np
from src.data_classes.common_data import SweepType
from src.data_classes.meta_data import MetaData


def export(path_to_file: str, metadata: MetaData):
    # exporting csv files
    with open(path_to_file, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(_generate_header(metadata=metadata))
        writer.writerows(_generate_data_in_columnar_form(metadata=metadata))


def _generate_header(metadata: MetaData) -> List[str]:
    header = [metadata.common_data.measuring_unit]
    for ch in range(metadata.common_data.channel_count):
        if metadata.common_data.sweep_type == SweepType.episodic:
            measuring_unit = {d.measuring_unit for d in metadata.data if d.ch == ch}
        else:
            measuring_unit = [d.measuring_unit for d in metadata.data if d.ch == ch]
        header.extend(measuring_unit)
    return header


def _generate_data_in_columnar_form(metadata: MetaData) -> ndarray:
    different_file_paths = {d.filepath for d in metadata.data}
    for file_path in different_file_paths:
        data_with_same_file_path = list(filter(lambda x: x.filepath == file_path, metadata.data))
        # episodic
        if len(data_with_same_file_path) > 1:
            episodic_data = np.tile(metadata.common_data.x, metadata.common_data.sweep_count)
            # group data in same channels have different measuring units
            for ch in range(metadata.common_data.channel_count):
                data_with_same_channel = [d for d in data_with_same_file_path if d.ch == ch]
                sorted_data = sorted(data_with_same_channel, key=lambda data: data.sweep_number)
                y = np.array([])
                for d in sorted_data:
                    y = np.concatenate((y, d.y), axis=None)
                episodic_data = np.vstack((episodic_data, y))
            return np.transpose(episodic_data)
        gap_free_data = metadata.common_data.x
        for ch in range(metadata.common_data.channel_count):
            data_with_same_channel = [d for d in data_with_same_file_path if d.ch == ch]
            sorted_data = sorted(data_with_same_channel, key=lambda data: data.sweep_number)
            y = np.array([])
            for d in sorted_data:
                y = np.vstack((y, d.y))
            episodic_data = np.vstack((episodic_data, y))
        return gap_free_data
