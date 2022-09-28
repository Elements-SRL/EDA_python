import pyabf
from pyabf import ABF

from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import CommonData, SweepType
from src.data_classes.meta_data import MetaData


def extract_meta_data_from_abf(path_to_file: str, metadata: MetaData):
    abf = pyabf.ABF(path_to_file)
    expected_length = round(abf.sampleRate * abf.sweepIntervalSec)
    cd: CommonData | None = None
    for ch in range(abf.channelCount):
        for sweep in range(abf.sweepCount):
            if cd is None:
                cd = CommonData(x=abf.sweepX[:expected_length],
                                sampling_rate=abf.sampleRate,
                                channel_count=abf.channelCount,
                                sweep_type=SweepType.episodic,
                                )
            abf.setSweep(sweepNumber=sweep, channel=ch)
            metadata.add_data(BasicData(ch=ch, y=abf.sweepY[:expected_length], sweep_number=sweep, measuring_unit=abf.sweepUnitsY))
    metadata.add_common_data(cd)
