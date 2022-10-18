from ordered_set import OrderedSet
from pyabf import ABF
from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup
from src.metadata.meta_data import MetaData


def extract_meta_data_from_abf(path_to_file: str, metadata: MetaData):
    basic_data = extract_basic_data(path_to_file)
    metadata.add_data_group(extract_data_group(basic_data=basic_data, path_to_file=path_to_file))


def extract_basic_data(path_to_file: str) -> OrderedSet[BasicData]:
    abf = ABF(path_to_file)
    expected_length = round(abf.sampleRate * abf.sweepIntervalSec)
    basic_data = OrderedSet()
    for ch in range(abf.channelCount):
        for sweep in range(abf.sweepCount):
            abf.setSweep(channel=ch, sweepNumber=sweep)
            name = abf.abfID[:5] if abf.sweepCount == 1 else abf.abfID[:5] + " ch " + str(ch) + " sw " + str(sweep)
            basic_data.add(BasicData(axis=ch, y=abf.sweepY[:expected_length], sweep_number=sweep, ch=ch,
                                     measuring_unit=abf.sweepUnitsY, file_path=abf.abfFilePath, name=name))
    return basic_data


def extract_data_group(path_to_file: str, basic_data: OrderedSet[BasicData]) -> DataGroup:
    abf = ABF(path_to_file)
    expected_length = round(abf.sampleRate * abf.sweepIntervalSec)
    abf.setSweep(sweepNumber=0, channel=0)
    dg = DataGroup(x=[abf.sweepX[:expected_length]], sampling_rate=abf.sampleRate, channel_count=abf.channelCount,
                   sweep_count=abf.sweepCount, measuring_unit=abf.sweepUnitsX, sweep_label_x=abf.sweepLabelX,
                   sweep_label_y=abf.sweepLabelY, sweep_label_c=abf.sweepLabelC, basic_data=basic_data,
                   name=abf.abfID)
    return dg
