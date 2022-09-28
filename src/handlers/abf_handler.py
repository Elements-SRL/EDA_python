import pyabf
from pyabf import ABF

from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import CommonData
from src.data_classes.meta_data import MetaData


def extract_meta_data_from_abf(path_to_file: str, metadata: MetaData):
    abf = pyabf.ABF(path_to_file)
    """multi sweep abf"""
    if abf.sweepCount > 1:
        return extract_multi_sweep_abf(abf, metadata)
    """mono sweep abf"""
    cd = CommonData(abf.sweepX, abf.sampleRate, abf.channelCount, abf.sweepUnitsX, abf.sweepUnitsY, abf.sweepUnitsC)
    metadata.add_common_data(cd)
    metadata.add_data(BasicData(0, y=abf.sweepY))
    if abf.data.size > 1:
        metadata.add_data(BasicData(1, abf.data[1]))


# display only sweeps of equal length
def extract_multi_sweep_abf(abf: ABF, metadata: MetaData):
    expected_length = round(abf.sampleRate * abf.sweepIntervalSec)
    cd: CommonData | None = None
    for ch in range(abf.channelCount):
        for sweep in range(abf.sweepCount):
            if cd is None:
                metadata.add_common_data(CommonData(x=abf.sweepX[:expected_length],
                                                    sampling_rate=abf.sampleRate,
                                                    channel_count=abf.channelCount,
                                                    unit_x=abf.sweepUnitsX,
                                                    unit_y=abf.sweepUnitsY,
                                                    unit_c=abf.sweepUnitsC,
                                                    ))
            abf.setSweep(sweep, ch)
            metadata.add_data(BasicData(ch=ch, y=abf.sweepY[:expected_length], sweep_number=sweep))
