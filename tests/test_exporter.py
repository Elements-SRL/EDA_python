import os.path
import unittest
import src.exporters.exporter as exporter
from src.logics.logics import Logics


class ExplorerTest(unittest.TestCase):
    # ABF
    path_to_basic_abf = "res/Data/Data_CH001_000.abf"

    path_to_contiguous_abf1 = "res/ContiguousData/temp_CH001_000.abf"
    path_to_contiguous_abf2 = "res/ContiguousData/temp_CH001_001.abf"
    path_to_contiguous_abf3 = "res/ContiguousData/temp_CH001_002.abf"

    path_to_episodic_abf = "res/EpisodicData/episodic several sweeps.abf"

    # EDH
    path_to_basic_edh = "res/Data/Data.edh"
    path_to_contiguous_edh = "res/ContiguousData/temp.edh"

    # CSV
    path_to_csv = "res/Data/test_export.csv"
    path_to_csv_of_contiguous_abfs = "res/ContiguousData/test_export.csv"
    path_to_csv_of_episodic_data = "res/EpisodicData/test_export.csv"
    path_to_basic_edh_csv = "res/Data/test_export_basic_edh.csv"
    path_to_csv_of_hist = "res/Data/test_hist.csv"

    fitting_params_csv = "res/Data/test_export_fitting_params.csv"

    episodic_abf_bugged = "res/EpisodicData/22919002.abf"
    episodic_abf_bugged_csv = "res/EpisodicData/22919002.csv"

    def test_generate_header(self):
        test_logics = Logics()
        test_logics.open(self.path_to_episodic_abf)
        print(exporter._generate_header(test_logics.metadata))

    def test_generate_header_episodic(self):
        test_logics = Logics()
        test_logics.open(self.path_to_episodic_abf)
        measuring_units = exporter._generate_header(test_logics.metadata)
        self.assertTrue(len(measuring_units) == 3)
        self.assertTrue("sec" in measuring_units)
        self.assertTrue("nA" in measuring_units)
        self.assertTrue("mV" in measuring_units)

    def test_generate_header_gap_free_from_single_abf(self):
        test_logics = Logics()
        test_logics.open(self.path_to_basic_abf)
        measuring_units = exporter._generate_header(test_logics.metadata)
        self.assertTrue(len(measuring_units) == 3)
        self.assertTrue("sec" in measuring_units[0])
        self.assertTrue("pA" in measuring_units[1])
        self.assertTrue("mV" in measuring_units[2])

    def test_generate_header_gap_free_from_edh_composed_by_single_abf(self):
        test_logics = Logics()
        test_logics.open(self.path_to_basic_edh)
        measuring_units = exporter._generate_header(test_logics.metadata)
        self.assertTrue(len(measuring_units) == 6)
        self.assertTrue("sec" in measuring_units[0])
        self.assertTrue("pA" in measuring_units[1])
        self.assertTrue("mV" in measuring_units[2])
        self.assertTrue("pA" in measuring_units[len(measuring_units) - 1])

    def test_generate_header_gap_free_from_edh_composed_contiguous_abf(self):
        test_logics = Logics()
        test_logics.open(self.path_to_basic_edh)
        measuring_units = exporter._generate_header(test_logics.metadata)
        self.assertTrue(len(measuring_units) == 6)
        self.assertTrue("sec" in measuring_units[0])
        self.assertTrue("pA" in measuring_units[1])
        self.assertTrue("mV" in measuring_units[2])
        self.assertTrue("pA" in measuring_units[len(measuring_units) - 1])

    def test_generate_data_episodic(self):
        test_logics = Logics()
        test_logics.open(self.path_to_episodic_abf)
        episodic_data = exporter._generate_data_in_columnar_form(test_logics.metadata)
        num_rows, num_cols = episodic_data.shape
        self.assertTrue(num_cols == 3)
        ch = 0
        data_with_same_measuring_unit = [
            d for d in test_logics.metadata.selected_data_group.basic_data if d.ch == ch
        ]
        sorted_data = sorted(
            data_with_same_measuring_unit, key=lambda data: data.sweep_number
        )
        i = 0
        for sd in sorted_data:
            self.assertTrue(sd.sweep_number == i)
            i += 1

    def test_export_episodic_data(self):
        test_logics = Logics()
        test_logics.open(self.path_to_episodic_abf)
        test_logics.export(path_to_file=self.path_to_csv_of_episodic_data)
        self.assertTrue(os.path.exists(self.path_to_csv_of_episodic_data))

    def test_export_basic_abf(self):
        test_logics = Logics()
        test_logics.open(self.path_to_basic_abf)
        test_logics.export(path_to_file=self.path_to_csv)
        self.assertTrue(os.path.exists(self.path_to_csv))

    def test_export_basic_edh(self):
        test_logics = Logics()
        test_logics.open(self.path_to_basic_edh)
        test_logics.export(path_to_file=self.path_to_basic_edh_csv)
        self.assertTrue(os.path.exists(self.path_to_basic_edh_csv))

    def test_export_contiguous_edh(self):
        test_logics = Logics()
        test_logics.open(self.path_to_contiguous_edh)
        test_logics.export(path_to_file=self.path_to_csv_of_contiguous_abfs)
        self.assertTrue(os.path.exists(self.path_to_csv_of_contiguous_abfs))

    def test_export_histogram(self):
        test_logics = Logics()
        test_logics.open(self.path_to_basic_edh)
        test_logics.hist()
        test_logics.export(path_to_file=self.path_to_csv_of_hist)
        self.assertTrue(os.path.exists(self.path_to_csv_of_hist))

    def test_export_fitting_params(self):
        test_logics = Logics()
        test_logics.open(self.path_to_basic_edh)
        eq, fitting_params = test_logics.fit("linear")
        exporter.export_fitting_params_to_csv(self.fitting_params_csv, eq, fitting_params)
        self.assertTrue(os.path.exists(self.fitting_params_csv))

    def test_export_episodic_abf(self):
        test_logics = Logics()
        test_logics.open(self.episodic_abf_bugged)
        test_logics.create_roi(0.03, 0.2, sweeps_to_keep=[0], channels_to_keep = [0])
        test_logics.export(self.episodic_abf_bugged_csv)
        self.assertTrue(os.path.exists(self.episodic_abf_bugged_csv))


    def tearDown(self):
        if os.path.exists(self.path_to_csv_of_episodic_data):
            os.remove(self.path_to_csv_of_episodic_data)
        if os.path.exists(self.path_to_csv):
            os.remove(self.path_to_csv)
        if os.path.exists(self.path_to_csv_of_contiguous_abfs):
            os.remove(self.path_to_csv_of_contiguous_abfs)
        if os.path.exists(self.path_to_basic_edh_csv):
            os.remove(self.path_to_basic_edh_csv)
        if os.path.exists(self.path_to_csv_of_hist):
            os.remove(self.path_to_csv_of_hist)
        if os.path.exists(self.fitting_params_csv):
            os.remove(self.fitting_params_csv)
        if os.path.exists(self.episodic_abf_bugged_csv):
            os.remove(self.episodic_abf_bugged_csv)


if __name__ == "__main__":
    unittest.main()
