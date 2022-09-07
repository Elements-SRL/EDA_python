import unittest
from os.path import exists
import pyabf
from src import file_handler as fh


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_open_non_existing_abf_file(self):
        path_to_file = "C:\\NON_EXISTING_FILE.abf"
        if not exists(path_to_file):
            print("error")

        fh.open_abf()

        abf = pyabf.ABF(path_to_file)
        self.assertIsNone(abf)

    def test_open_existing_abf_file(self):
        path_to_file = "../res/Data_CH001_000.abf"
        if not exists(path_to_file):
            print("error")
            self.fail("No file should be found")
        else:
            if path_to_file.endswith(".abf"):
                abf = pyabf.ABF(path_to_file)
                self.assertIsNotNone(abf)

    def test_input(self):
        file_path = input("insert file path: ")
        if file_path.endswith(".abf"):
            print(file_path)
            self.assertEqual("ciccia","ciccia")

    def test_import(self):
        self.assertEqual(fh.open_file(), True)


if __name__ == '__main__':
    unittest.main()
