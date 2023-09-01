import unittest

import numpy as np

import src.analysis.filters.filter_handler
from src.analysis.filters.filter_arguments import FilterArguments
from src.logics.logics import Logics


class LogicsTest(unittest.TestCase):
    path_to_abf1 = "res/Data/Data_CH001_000.abf"
    path_to_abf2 = "res/Data/Data_CH002_000.abf"

    path_to_contiguous_abf1 = "res/ContiguousData/temp_CH001_000.abf"
    path_to_contiguous_abf2 = "res/ContiguousData/temp_CH001_001.abf"
    path_to_contiguous_abf3 = "res/ContiguousData/temp_CH001_002.abf"

    path_to_basic_edh = "res/Data/Data.edh"
    path_to_contiguous_edh = "res/ContiguousData/temp.edh"

    path_to_episodic_abf = "res/EpisodicData/episodic several sweeps.abf"
    path_to_csv = "res/Data/test_export.csv"
    path_to_csv_of_contiguous_abfs = "res/ContiguousData/test_export.csv"
    path_to_csv_of_episodic_data = "res/EpisodicData/test_export.csv"

    def test_open_first_abf(self):
        logics_test = Logics()
        logics_test.open(self.path_to_abf1)
        self.assertTrue(logics_test.metadata.selected_data_group.channel_count == 2)
        print(len(logics_test.metadata.selected_data_group.basic_data))
        self.assertTrue(len(logics_test.metadata.selected_data_group.basic_data) == 2)

    def test_common_data_from_abf(self):
        logics_test = Logics()
        logics_test.open(self.path_to_abf1)
        x = logics_test.metadata.get_x()
        self.assertTrue(len(x) > 1)

    def test_open_basic_edh(self):
        logics_test = Logics()
        logics_test.open(self.path_to_basic_edh)
        self.assertTrue(len(logics_test.metadata.selected_data_group.basic_data) == 5)
        # of all the data only one has the measuring unit mV
        data_in_mV = list(
            filter(lambda x: x.measuring_unit == "mV", logics_test.metadata.selected_data_group.basic_data))
        self.assertTrue(len(data_in_mV) == 1)
        # all the other data has the measuring unit pA
        data_in_mV = list(
            filter(lambda x: x.measuring_unit == "pA", logics_test.metadata.selected_data_group.basic_data))
        self.assertTrue(len(data_in_mV) == 4)
        self.assertTrue(
            len(logics_test.metadata.get_x()) ==
            len(logics_test.metadata.selected_data_group.basic_data.pop(0).y))
        self.assertTrue(logics_test.metadata.selected_data_group.channel_count == 4)

    def test_open_edh_with_contiguous_data(self):
        logics_test = Logics()
        logics_test.open(self.path_to_contiguous_edh)
        self.assertTrue(len(logics_test.metadata.selected_data_group.basic_data) == 5)
        self.assertTrue(logics_test.metadata.selected_data_group.channel_count == 4)

    def test_file_path_in_episodic_data(self):
        logics_test = Logics()
        logics_test.open(self.path_to_episodic_abf)
        file_path = logics_test.metadata.selected_data_group.basic_data[0].filepath
        for d in logics_test.metadata.selected_data_group.basic_data:
            self.assertTrue(d.filepath == file_path)

    def test_file_path_in_basic_edh(self):
        logics_test = Logics()
        logics_test.open(self.path_to_basic_edh)
        file_path_of_data_from_the_same_axis = {d.filepath for d in
                                                logics_test.metadata.selected_data_group.basic_data if d.axis == 0}
        self.assertTrue(len(file_path_of_data_from_the_same_axis) == 4)

    def test_filter(self):
        logics_test = Logics()
        logics_test.open(self.path_to_basic_edh)
        filter_args = FilterArguments(filter_type="butter",
                                      order=4,
                                      b_type="highpass",
                                      cutoff_frequency=0.5,
                                      analog=False,
                                      fs=2000)
        y = src.analysis.filters.filter_handler.filter_signal(filter_args,
                                                              y=logics_test.metadata.selected_data_group.basic_data[0].y)
        print(y)

    def test_filters(self):
        logics_test = Logics()
        logics_test.open(self.path_to_basic_edh)
        print(logics_test.metadata.selected_data_group.id)
        filter_args = FilterArguments(filter_type="butter",
                                      order=4,
                                      b_type="highpass",
                                      cutoff_frequency=500,
                                      analog=False,
                                      fs=2000,
                                      )
        logics_test.filter_selected_data_group(filter_args=filter_args)
        print(logics_test.metadata.selected_data_group.id)
        for d in logics_test.metadata.selected_data_group.basic_data:
            print(d.y)
        sdg = logics_test.metadata.selected_data_group
        print(sdg)
        self.assertTrue(len(sdg.basic_data) == 5)
        dg = logics_test.metadata.data_groups.pop()
        print(dg)
        self.assertTrue(len(dg.data_groups) != len(sdg.data_groups))
        filtered_dg = dg.data_groups.pop()
        print(filtered_dg)
        self.assertTrue(len(filtered_dg.data_groups) == 0)

    def test_operations(self):
        logics_test = Logics()
        logics_test.open(self.path_to_basic_edh)
        dg = logics_test.metadata.selected_data_group
        logics_test.perform_operations(list(dg.basic_data), dg.basic_data[0], "a-a")
        dg2 = logics_test.metadata.selected_data_group
        self.assertTrue(np.all(dg2.basic_data[0].y == np.zeros(len(dg2.basic_data[0].y))))


if __name__ == '__main__':
    unittest.main()
