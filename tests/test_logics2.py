import unittest
from src.logics2 import Logics2


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


if __name__ == '__main__':
    unittest.main()
