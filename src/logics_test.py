import unittest
import logics


class LogicsTest(unittest.TestCase):
    path_to_abf1 = "res/Data/Data_CH001_000.abf"
    path_to_abf2 = "res/Data/Data_CH002_000.abf"

    def test_open_first_abf(self):
        logics_test = logics.Logics()
        logics_test.open_abf(self.path_to_abf1)
        self.assertTrue(len(logics_test.abfs) == 1)

    def test_open_different_abf(self):
        logics_test = logics.Logics()
        logics_test.open_abf(self.path_to_abf1)
        logics_test.open_abf(self.path_to_abf2)
        self.assertTrue(len(logics_test.abfs) == 2)

    def test_open_same_abf(self):
        logics_test = logics.Logics()
        logics_test.open_abf(self.path_to_abf1)
        logics_test.open_abf(self.path_to_abf1)
        self.assertTrue(len(logics_test.abfs) == 1)

    def test_get_abfs_from_empty_list(self):
        logics_test = logics.Logics()
        abfs = logics_test.get_abfs()
        self.assertListEqual(abfs, [])

    def test_get_abfs(self):
        logics_test = logics.Logics()
        logics_test.open_abf(self.path_to_abf1)
        abfs = logics_test.get_abfs()
        self.assertTrue(len(abfs) == 1)

    def test_get_name(self):
        logics_test = logics.Logics()
        logics_test.open_abf(self.path_to_abf1)
        abfs = logics_test.get_abfs()
        channel_name = logics.get_channel_name(abfs[0])
        print(channel_name)
        self.assertEquals("channel 1", channel_name)


if __name__ == '__main__':
    unittest.main()
