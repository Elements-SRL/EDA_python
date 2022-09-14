import os
import time
import unittest
import logics


class LogicsTest(unittest.TestCase):
    path_to_abf1 = "res/Data/Data_CH001_000.abf"
    path_to_abf2 = "res/Data/Data_CH002_000.abf"

    def test_open_first_abf(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        self.assertTrue(len(logics_test.abfs) == 1)

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
        channel_name = logics.get_channel_name(abfs[0])
        self.assertEqual("channel 1", channel_name)

    def test_get_name_abbreviation(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        abfs = logics_test.get_abfs()
        channel_name = logics.get_channel_name_abbreviation(abfs[0])
        self.assertEqual("ch1", channel_name)

    def test_get_edh(self):
        logics_test = logics.Logics()
        logics_test.open("res/Data/Data.edh")
        self.assertTrue(len(logics_test.get_abfs()) == 4)

    # def test_generate_header_from_empty_list(self):
    #     logics_test = logics.Logics()
    #     header = logics_test.generate_header()
    #     self.assertIsNone(header)

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
        path_to_csv = "res/Data/test_export.csv"
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        logics_test.open(self.path_to_abf2)
        logics_test.export(path_to_csv)
        time.sleep(1)
        self.assertTrue(os.path.exists(path_to_csv))

    def test_hidden_abfs(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        logics_test.open(self.path_to_abf2)
        self.assertFalse(logics_test.hidden_channels)
        ch1 = "channel 1"
        logics_test.add_to_hidden_channels(ch1)
        self.assertTrue(logics_test.hidden_channels[0] == ch1)

    def test_toggle_visibility(self):
        logics_test = logics.Logics()
        ch1 = "ch1"
        ch2 = "ch2"
        logics_test.toggle_visibility(ch1)
        logics_test.toggle_visibility(ch2)
        self.assertTrue(ch1 in logics_test.hidden_channels)
        logics_test.toggle_visibility(ch1)
        self.assertTrue(ch1 not in logics_test.hidden_channels)

    def test_get_visible_abfs(self):
        logics_test = logics.Logics()
        logics_test.open(self.path_to_abf1)
        logics_test.open(self.path_to_abf2)
        self.assertTrue(len(logics_test.get_visible_abfs()) == 2)
        for ch in logics_test.names_to_abfs:
            logics_test.toggle_visibility(ch)
        self.assertTrue(len(logics_test.get_visible_abfs()) == 0)


if __name__ == '__main__':
    unittest.main()
