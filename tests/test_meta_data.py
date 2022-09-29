import unittest
import numpy as np
from src.data_classes.basic_data import BasicData
from src.data_classes.common_data import CommonData, SweepType
from src.data_classes.meta_data import MetaData


class MetaDataTest(unittest.TestCase):

    def test_metadata_creation(self):
        metadata = MetaData()
        self.assertTrue(not metadata.data)

    def test_add_basic_data(self):
        metadata = MetaData()
        bd = BasicData(ch=1, y=np.array([1, 2, 3]), measuring_unit="p")
        metadata.add_data(bd)
        self.assertTrue(len(metadata.data) == 1)

    def test_data_content(self):
        metadata = MetaData()
        arr = np.array([1, 2, 3])
        bd = BasicData(ch=1, y=arr, measuring_unit="p")
        metadata.add_data(bd)
        arr2 = metadata.data.pop().y
        self.assertListEqual(list(arr), list(arr2))

    def test_add_common_data(self):
        metadata = MetaData()
        cd = CommonData(x=np.array([1, 2, 3]), sampling_rate=10, channel_count=5, measuring_unit="s",
                        sweep_label_y="pA", sweep_label_c="mV", sweep_label_x="sec", sweep_type=SweepType.episodic)
        metadata.add_common_data(cd)
        self.assertTrue(len(metadata.common_data.x) == 3)
        self.assertTrue(metadata.common_data.channel_count == 5)
        self.assertTrue(metadata.common_data.sampling_rate == 10)

    def test_already_opened_file(self):
        metadata = MetaData()
        path = "path/to/file"
        metadata.add_path(path)
        metadata.add_data(BasicData(ch=1, y=np.array([1, 2, 3]), measuring_unit="p"))
        self.assertTrue(metadata.already_opened(path))

