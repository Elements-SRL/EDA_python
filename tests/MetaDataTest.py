import unittest

import numpy as np

from src.data_classes.basic_data import BasicData
from src.data_classes.meta_data import MetaData


class MetaDataTest(unittest.TestCase):

    def test_metadata_creation(self):
        metadata = MetaData()
        self.assertTrue(not metadata.data)

    def test_add_basic_data(self):
        metadata = MetaData()
        bd = BasicData(1, np.array([1, 2, 3]))
        metadata.add_data(bd)
        self.assertTrue(len(metadata.data) == 1)
