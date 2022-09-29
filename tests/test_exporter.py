import unittest
import src.exporter as exporter
from src.logics2 import Logics2


class ExplorerTest(unittest.TestCase):
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

    def test_generate_header(self):
        test_logics = Logics2()
        test_logics.open(self.path_to_episodic_abf)
        print(exporter._generate_header(test_logics.metadata))

    def test_generate_header_episodic(self):
        test_logics = Logics2()
        test_logics.open(self.path_to_episodic_abf)
        measuring_units = exporter._generate_header(test_logics.metadata)
        self.assertTrue(len(measuring_units) == 3)
        self.assertTrue("sec" in measuring_units)
        self.assertTrue("nA" in measuring_units)
        self.assertTrue("mV" in measuring_units)


if __name__ == '__main__':
    unittest.main()
