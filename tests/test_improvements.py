import math
import time
import unittest
from concurrent.futures import ProcessPoolExecutor

import matplotlib.pyplot as plt
import numpy as np

from src.logics.logics import Logics


class LogicsTest(unittest.TestCase):
    path_to_basic_edh = "/home/luca/EDA_python/res/Data/Data.edh"
    path_to_choncky_abf = "/home/luca/data_tirocionio/test/20220405_3M_KCl_K239A_10C_140mv_00300_CH01_corr_CH001_001.abf"

    def test_open_basic_edh(self):
        logics_test = Logics()
        logics_test.open(self.path_to_choncky_abf)
        start = time.time()
        fig, ax = plt.subplots()
        orig_y = logics_test.metadata.selected_data_group.basic_data.pop(0).y
        orig_x = logics_test.metadata.selected_data_group.x
        # ax.plot(orig_x, orig_y)
        pixels = 4096 * 2
        factor = math.floor(orig_y.size / pixels)
        y = orig_y[:factor * pixels]
        y = np.reshape(y, (pixels, factor))
        # find min and max
        maxes = y.max(1)
        mins = y.min(1)
        # put min and max together
        y = np.vstack((mins, maxes))
        # transpose matrix
        y = np.transpose(y)
        # reshape to one dimension
        y = np.reshape(y, pixels * 2)
        x = orig_x[:factor * pixels: factor // 2]
        end = time.time()
        print(end - start)
        # ax.plot(x, y)
        # plt.show()

    def test_draw_better(self):
        logics_test = Logics()
        logics_test.open(self.path_to_choncky_abf)
        fig, ax = plt.subplots()
        start = time.time()
        orig_y = logics_test.metadata.selected_data_group.basic_data.pop(0).y
        orig_x = logics_test.metadata.selected_data_group.x
        # ax.plot(orig_x, orig_y)
        pixels = 4096 * 2
        factor = math.floor(orig_y.size / pixels)
        y = orig_y[:factor * pixels]
        y = np.reshape(y, (pixels, factor))
        # find min and max
        # put min and max together
        # transpose matrix
        # reshape to one dimension
        y = np.reshape(np.transpose(np.vstack((y.min(1), y.max(1)))), pixels * 2)
        x = orig_x[:factor * pixels: factor // 2]
        end = time.time()
        print(end - start)
        # ax.plot(x, y)
        # plt.show()

    def test_no_ops(self):
        logics_test = Logics()
        logics_test.open(self.path_to_choncky_abf)
        fig, ax = plt.subplots()
        orig_y = logics_test.metadata.selected_data_group.basic_data.pop(0).y
        orig_x = logics_test.metadata.selected_data_group.x
        # ax.plot(orig_x, orig_y)
        # plt.show()

    def test_process_data(self):
        y = np.array([1,2,3,4,5,6,7,8,9,1,2,3,4,5])
        pixels = 4
        factor = 3
        y = y[:factor * pixels]
        y = np.reshape(y, (pixels, factor))
        print(y)
        maxes = y.max(1)
        mins = y.min(1)
        print(mins, maxes)
        y = np.vstack((mins, maxes))
        y = np.transpose(y)
        print(y)
        y = np.reshape(y, pixels * 2)
        print("almost there")
        print(y.size)

    def test_shit(self):
        with ProcessPoolExecutor() as executor:
            # for line in self.lines:
            # line.line.set_data(*executor.map(self.simplify, idx_of_min, idx_of_max, line))
            # line.ax.figure.canvas.draw_idle()
            executor.map(say_hi, ["ciccia", "culo"])


def say_hi(arg):
    print("hello "+ arg)


if __name__ == '__main__':
    unittest.main()
