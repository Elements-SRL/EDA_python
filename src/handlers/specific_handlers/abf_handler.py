from pyabf import ABF
from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.common_data import CommonData
from src.metadata.meta_data import MetaData


def extract_meta_data_from_abf(path_to_file: str, metadata: MetaData):
    abf = ABF(path_to_file)
    expected_length = round(abf.sampleRate * abf.sweepIntervalSec)
    cd: CommonData | None = None
    for ch in range(abf.channelCount):
        for sweep in range(abf.sweepCount):
            if cd is None:
                cd = CommonData(x=abf.sweepX[:expected_length], sampling_rate=abf.sampleRate,
                                channel_count=abf.channelCount, sweep_count=abf.sweepCount,
                                measuring_unit=abf.sweepUnitsX, sweep_label_x=abf.sweepLabelX,
                                sweep_label_y=abf.sweepLabelY, sweep_label_c=abf.sweepLabelC,
                                )
            abf.setSweep(sweepNumber=sweep, channel=ch)
            metadata.add_data(BasicData(ch=ch, y=abf.sweepY[:expected_length], sweep_number=sweep,
                                        measuring_unit=abf.sweepUnitsY, file_path=abf.abfFilePath))
    metadata.add_common_data(cd)
