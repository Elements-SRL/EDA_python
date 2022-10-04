import unittest
from src.logics import Logics


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
        print(len(logics_test.metadata.selected_data_group.basic_data))
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
            len(logics_test.metadata.selected_data_group.x) ==
            len(logics_test.metadata.selected_data_group.basic_data.pop(0).y))

    def test_open_edh_with_contiguous_data(self):
        logics_test = Logics()
        logics_test.open(self.path_to_contiguous_edh)
        print(len(logics_test.metadata.selected_data_group.basic_data))
        for d in logics_test.metadata.selected_data_group.basic_data:
            print(d)
        self.assertTrue(len(logics_test.metadata.selected_data_group.basic_data) == 5)

    def test_file_path_in_episodic_data(self):
        logics_test = Logics()
        logics_test.open(self.path_to_episodic_abf)
        file_path = logics_test.metadata.selected_data_group.basic_data[0].filepath
        for d in logics_test.metadata.selected_data_group.basic_data:
            self.assertTrue(d.filepath == file_path)

    def test_file_path_in_basic_edh(self):
        logics_test = Logics()
        logics_test.open(self.path_to_basic_edh)
        file_path_of_data_from_the_same_channel = {d.filepath for d in
                                                   logics_test.metadata.selected_data_group.basic_data if d.ch == 0}
        self.assertTrue(len(file_path_of_data_from_the_same_channel) == 4)


if __name__ == '__main__':
    unittest.main()
