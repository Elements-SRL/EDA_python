import struct
import numpy as np
from ordered_set import OrderedSet
from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup
from src.metadata.meta_data import MetaData
import os

def extract_metadata_from_dat(path_to_dat: str, metadata: MetaData):
    f = open(path_to_dat, "rb")
    f_cont = f.read()
    f.close()
    raw = struct.unpack("d" * (len(f_cont) // 8), f_cont)
    y = np.array(raw)
    # print("raw calculated")
    x = np.linspace(0, len(y), len(y))
    # print("x calculated")
    bd_os: OrderedSet[BasicData] = OrderedSet()
    name = path_to_dat.split(os.sep).pop()
    bd = BasicData(ch=0, y=y, measuring_unit="A", sweep_number=0, file_path=path_to_dat,
                                 name=name, axis=0)
    bd_os.add(bd)
    dg = DataGroup(x=x, sampling_rate=250000, channel_count=1, sweep_count=1, measuring_unit="s", sweep_label_x="sec", sweep_label_y="Current A", sweep_label_c="*", name=name, type="raw", basic_data=bd_os)
    metadata.add_data_group(dg)