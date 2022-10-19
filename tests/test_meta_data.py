import unittest
import numpy as np
from ordered_set import OrderedSet

from src.metadata.data_classes.basic_data import BasicData
from src.metadata.data_classes.data_group import DataGroup
from src.metadata.meta_data import MetaData


class MetaDataTest(unittest.TestCase):

    def test_metadata_creation(self):
        metadata = MetaData()
        self.assertTrue(not metadata.data_groups)

    def test_add_common_data(self):
        metadata = MetaData()
        arr = np.array([1, 2, 3])
        bd = BasicData(ch=1, y=arr, measuring_unit="p", file_path="path/to/file", name="name", axis=0)
        dg = DataGroup(x=arr, sampling_rate=10, channel_count=5, measuring_unit="s",
                       sweep_label_y="pA", sweep_label_c="mV", sweep_label_x="sec", sweep_count=5,
                       basic_data=OrderedSet([bd]), name="ciccia", type="raw",
                       )
        metadata.add_data_group(dg)
        self.assertTrue(len(metadata.get_x()) == len(dg.x))
        self.assertTrue(metadata.selected_data_group.channel_count == 5)
        self.assertTrue(metadata.selected_data_group.sampling_rate == 10)

    def test_add_same_element_two_times(self):
        metadata = MetaData()
        arr = np.array([1, 2, 3])
        bd = BasicData(ch=1, y=arr, measuring_unit="p", file_path="path/to/file", name="name", axis=0)
        dg = DataGroup(x=np.array([1, 2, 3]), sampling_rate=10, channel_count=5, measuring_unit="s",
                       sweep_label_y="pA", sweep_label_c="mV", sweep_label_x="sec", sweep_count=5,
                       basic_data=OrderedSet([bd]), name="ciccia", type="raw",
                       )
        metadata.add_data_group(dg)
        metadata.add_data_group(dg)
        self.assertTrue(len(metadata.data_groups) == 1)
        self.assertTrue(metadata.selected_data_group.id == 0)

    def test_add_different_data_groups(self):
        metadata = MetaData()
        arr = np.array([1, 2, 3])
        bd = BasicData(ch=1, y=arr, measuring_unit="p", file_path="path/to/file", name="name", axis=0)
        dg = DataGroup(x=np.array([1, 2, 3]), sampling_rate=10, channel_count=5, measuring_unit="s",
                       sweep_label_y="pA", sweep_label_c="mV", sweep_label_x="sec", sweep_count=5,
                       basic_data=OrderedSet([bd]), name="ciccia", type="raw",
                       )
        arr2 = np.array([1, 2, 3, 4, 5])
        bd2 = BasicData(ch=1, y=arr2, measuring_unit="p", file_path="path/to/file", name="name", axis=0)
        dg2 = DataGroup(x=np.array([1, 2, 3]), sampling_rate=10, channel_count=5, measuring_unit="s",
                        sweep_label_y="pA", sweep_label_c="mV", sweep_label_x="sec", sweep_count=5,
                        basic_data=OrderedSet([bd2]), name="ciccia", type="raw",
                        )
        metadata.add_data_group(dg)
        metadata.add_data_group(dg2)
        self.assertTrue(len(metadata.data_groups) == 2)
        self.assertTrue(metadata.selected_data_group.id == 1)
