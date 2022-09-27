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
        x = logics_test.get_x()
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

    def test_open_different_abf(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        logics_test.open(self.path_to_abf2)
        self.assertTrue(len(logics_test.abfs) == 2)

    def test_open_same_abf(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        logics_test.open(self.path_to_abf1)
        self.assertTrue(len(logics_test.abfs) == 1)

    def test_get_abfs_from_empty_list(self):
        logics_test = logics.Logics()
        abfs = logics_test.get_abfs()
        self.assertListEqual(abfs, [])

    def test_get_abfs(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        abfs = logics_test.get_abfs()
        self.assertTrue(len(abfs) == 1)

    def test_get_name(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        abfs = logics_test.get_abfs()
        channel_name = logics.channel_name(abfs[0])
        self.assertEqual("channel 1", channel_name)

    def test_get_name_abbreviation(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        abfs = logics_test.get_abfs()
        channel_name = logics.channel_name_abbreviation(abfs[0])
        self.assertEqual("ch1", channel_name)

    def test_get_edh(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_basic_edh)
        self.assertTrue(len(logics_test.get_abfs()) == 4)

    def test_generate_header(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        logics_test.open(self.path_to_abf2)
        header = logics_test.generate_header()
        self.assertListEqual(["t[sec]", 'ch1[pA]', 'vC1[mV]', 'ch2[pA]', 'vC2[mV]'], header)

    def test_export_empty_csv(self):
        test_empty_csv = "res/Data/test_empty.csv"
        logics_test = logics.Logics()
        logics_test.export(test_empty_csv)
        self.assertFalse(os.path.exists(test_empty_csv))

    def test_export_csv(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        logics_test.open(self.path_to_abf2)
        logics_test.export(self.path_to_csv)
        time.sleep(1)
        self.assertTrue(os.path.exists(self.path_to_csv))

    def test_hidden_abfs(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        logics_test.open(self.path_to_abf2)
        self.assertFalse(logics_test.hidden_channels)
        ch1 = "channel 1"
        logics_test.set_channel_visibility(ch1, False)
        self.assertTrue(ch1 in logics_test.hidden_channels)
        logics_test.set_channel_visibility(ch1, True)
        self.assertTrue(ch1 not in logics_test.hidden_channels)

    def test_get_visible_abfs(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        logics_test.open(self.path_to_abf2)
        self.assertTrue(len(logics_test.get_visible_abfs()) == 2)
        for ch in logics_test.names_to_abfs:
            logics_test.set_channel_visibility(ch, False)
        self.assertTrue(len(logics_test.get_visible_abfs()) == 0)

    def test_open_contiguous_abf(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_contiguous_abf1)
        logics_test.open(self.path_to_contiguous_abf2)
        logics_test.open(self.path_to_contiguous_abf3)
        total_sweepX = 0
        total_sweepY = 0
        total_sweepC = 0
        for abf in logics_test.get_abfs():
            total_sweepX += len(abf.sweepX)
            total_sweepY += len(abf.sweepY)
            total_sweepC += len(abf.sweepC)
        logics_test.clear()

        logics_test.open_contiguous_abf(
            [self.path_to_contiguous_abf1, self.path_to_contiguous_abf2, self.path_to_contiguous_abf3])
        self.assertTrue(total_sweepX == len(logics_test.abfs[0].sweepX))
        self.assertTrue(total_sweepY == len(logics_test.abfs[0].sweepY))
        self.assertTrue(total_sweepC == len(logics_test.abfs[0].sweepC))

    def test_are_abfs_contiguous(self):
        self.assertTrue(logics.are_files_contiguous(
            [self.path_to_contiguous_abf1, self.path_to_contiguous_abf2, self.path_to_contiguous_abf3]))

    def test_open_contiguous_abfs(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_contiguous_edh)
        self.assertTrue(len(logics_test.get_abfs()) == 4)

    def test_export_contiguous_abfs(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_contiguous_edh)
        logics_test.export(self.path_to_csv_of_contiguous_abfs)
        time.sleep(1)
        self.assertTrue(os.path.exists(self.path_to_csv_of_contiguous_abfs))

    # TODO could be tested a little bit more accurately
    def test_generate_multi_sweep_data(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_episodic_abf)
        logics_test.export(self.path_to_csv_of_episodic_data)
        self.assertGreater(os.path.getsize(self.path_to_csv_of_episodic_data), 2_000_000)

    # def tearDown(self):
    #     if os.path.exists(self.path_to_csv):
    #         os.remove(self.path_to_csv)
    #     if os.path.exists(self.path_to_csv_of_contiguous_abfs):
    #         os.remove(self.path_to_csv_of_contiguous_abfs)
    #     if os.path.exists(self.path_to_csv_of_episodic_data):
    #         os.remove(self.path_to_csv_of_episodic_data)

    def test_file(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_episodic_abf)
        print(logics_test.get_abfs()[0].headerText)


if __name__ == '__main__':
    unittest.main()
