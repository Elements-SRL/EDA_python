import unittest
import numpy as np
from src.metadata.data_classes.basic_data import BasicData


class TestBasicData(unittest.TestCase):

    def test_data_creation(self):
        channel = 1
        arr = np.array([1, 2, 3])
        bd = BasicData(channel, arr, "m", file_path="path/to/file", name="charles")
        self.assertTrue(bd.ch == channel)
        self.assertTrue(bd.y[0] == arr[0])


if __name__ == '__main__':
    unittest.main()
