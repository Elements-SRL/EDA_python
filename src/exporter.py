import csv
from typing import List

from src.data_classes.meta_data import MetaData


def export(path_to_file: str, metadata: MetaData):
    # exporting csv files
    with open(path_to_file, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(generate_header(metadata=metadata))
        data = generate_data(metadata=metadata)
        writer.writerows(data)


def generate_header(metadata: MetaData) -> List[str]:
    header = ["t[" + metadata.common_data.unit_x + "]"]
    for ch in range(metadata.common_data.channel_count):
        header.append("[" + metadata.common_data.unit_y + "]")
        header.append("[" + metadata.common_data.unit_c + "]")
    return header


def generate_data(metadata: MetaData) -> List[List[float]]:
    pass
