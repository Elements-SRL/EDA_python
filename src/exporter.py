import csv
from typing import List

from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import SweepType
from src.data_classes.meta_data import MetaData


def export(path_to_file: str, metadata: MetaData):
    # exporting csv files
    with open(path_to_file, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(_generate_header(metadata=metadata))
        data = _generate_data(metadata=metadata)
        writer.writerows(data)


def _generate_header(metadata: MetaData) -> List[str]:
    header = [metadata.common_data.measuring_unit]
    if metadata.common_data.sweep_type == SweepType.episodic:
        different_measuring_units = {d.measuring_unit for d in metadata.data}
        return header + list(different_measuring_units)

    return header


def _generate_data(metadata: MetaData) -> List[List[float]]:
    pass
