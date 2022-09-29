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
        data = _generate_data(metadata=metadata)
        writer.writerows(data)


def _generate_header(metadata: MetaData) -> List[str]:
    header = [metadata.common_data.measuring_unit]
    if metadata.common_data.sweep_type == SweepType.episodic:
        different_measuring_units = {d.measuring_unit for d in metadata.data}
        return header + list(different_measuring_units)
    measuring_units = [d.measuring_unit for d in metadata.data]
    measuring_units.sort()
    return header + measuring_units


def _generate_data(metadata: MetaData) -> List[List[float]]:
    pass
    # return _format_to_csv()

    # data_to_export = metadata.common_data.x
    # different_measuring_units = {d.measuring_unit for d in metadata.data}



def _arrange_episodic_data(metadata: MetaData) -> List[ndarray]:
    pass


def _format_to_csv(data: List[ndarray]):
    # create matrix with all data
    arrays = np.array(data)

    # array with this form
    # [[t1,t2,..tn],
    #  [ch1_1, ch1_2.., ch1_n],
    #  [vC1_1, vC1_2,.., vC1_n],
    #  .
    #  .
    #  [chn_1, chn_2.., chn_n],
    #  [vCn_1, vCn_2,.., vCn_n]]

    formatted_data = []
    # for each value of time the get the corresponding data
    for i in range(len(data[0])):
        row = arrays[:, i]
        formatted_data.append(row)

    # now data is in the form
    # [[t1, ch1_1, vC1_1, .. chn_1, vCN_1],
    #  [t2, ch1_2, vC1_2, .. chn_2, vCN_2],
    #   .
    #   .
    #   [tn, ch1_n, vC1_n, .. chn_n, vCN_n]]
    return formatted_data
