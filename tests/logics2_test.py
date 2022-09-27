import sys

# importing

sys.path.append("../src")
from src.logics2 import Logics2
import unittest


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
        logics_test = Logics2()
        logics_test.open(self.path_to_abf1)
        self.assertTrue(len(logics_test.metadata.data) == 2)

    def test_common_data_from_abf(self):
        logics_test = Logics2()
        logics_test.open(self.path_to_abf1)
        x = logics_test.metadata.get_x()
        self.assertTrue(len(x) > 1)

    def test_get_all_y(self):
        logics_test = Logics2()
        logics_test.open(self.path_to_abf1)
        ch_to_y_values = logics_test.get_y()
        self.assertTrue(isinstance(ch_to_y_values, list))

    def test_get_y_by_channel(self):
        logics_test = Logics2()
        logics_test.open(self.path_to_abf1)
        l_temp = logics_test.get_y(0)
        _, y = l_temp.pop()
        self.assertTrue(isinstance(y, list))

    def test_get_y_with_wrong_channel(self):
        logics_test = Logics2()
        logics_test.open(self.path_to_abf1)
        not_existing_channel = 69
        ch_to_y = logics_test.get_y(not_existing_channel)
        self.assertTrue(isinstance(ch_to_y, list))
        for d in ch_to_y:
            x, y = d
            self.assertTrue(isinstance(x, int))
            self.assertTrue(isinstance(y, list))

    def test_x_and_y_correctness(self):
        logics_test = Logics2()
        logics_test.open(self.path_to_abf1)
        ch_to_y_sweeps = logics_test.get_y()
        x = logics_test.get_x()
        for t in ch_to_y_sweeps:
            _, y_sweeps = t
            for y in y_sweeps:
                self.assertTrue(len(x) == len(y))

    def test_open_multi_sweep(self):
        logics_test = Logics2()
        logics_test.open(self.path_to_episodic_abf)
        ch_to_y_sweeps = logics_test.get_y()
        x = logics_test.get_x()
        for tup in ch_to_y_sweeps:
            _, y_values = tup
            self.assertTrue(len(y_values) == 15)
            for y in y_values:
                self.assertTrue(len(y) == len(x))
                

if __name__ == '__main__':
    unittest.main()
