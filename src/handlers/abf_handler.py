import pyabf

from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import CommonData
from src.data_classes.meta_data import MetaData


def extract_meta_data_from_abf(path_to_file: str, metadata: MetaData):
    abf = pyabf.ABF(path_to_file)
    """multi sweep abf"""
    if abf.sweepCount > 1:
        return extract_multi_sweep_abf()
    """mono sweep abf"""
    cd = CommonData(abf.sweepX, abf.sampleRate, abf.channelCount)
    metadata.add_common_data(cd)
    print("fok")
    metadata.add_data(BasicData(0, abf.sweepY))
    if abf.data.size > 1:
        print("qui")
        metadata.add_data(BasicData(1, abf.data[1]))


def extract_multi_sweep_abf() -> MetaData:
    pass
