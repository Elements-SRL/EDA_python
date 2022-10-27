import time
from concurrent.futures import ThreadPoolExecutor
import math
from typing import List

import numpy as np
from numpy import ndarray

from src.plot_simplifier.line import Line


class SimplifierBrain:

    def __init__(self, xdata: ndarray, lines: List[Line]):
        self.idx_of_max = None
        self.idx_of_min = None
        self.lines = lines
        self.x_data = xdata
        print(len(lines))
        self.pixels = 4096 * 2

    def setup(self):
        self.compute(idx_of_min=0, idx_of_max=self.x_data.size - 1)

    def simplify(self, line: Line):
        start = time.time()
        # print("inside simplify")
        x = self.x_data[self.idx_of_min: self.idx_of_max]
        y = line.y[self.idx_of_min: self.idx_of_max]
        if x.size < self.pixels or math.floor(x.size / self.pixels) / 2 < 1:
            # print("shortcut")
            return x, y
        factor = math.floor(y.size / self.pixels)
        y = y[:factor * self.pixels]
        y = np.reshape(y, (self.pixels, factor))
        # find min and max
        # put min and max together
        # transpose matrix
        # reshape to one dimension
        y = np.reshape(np.transpose(np.vstack((y.min(1), y.max(1)))), self.pixels * 2)
        x = x[:: factor // 2]
        end = time.time()
        print(end - start)
        return x[:self.pixels * 2], y
        # callbacks.process('draw_event', DrawEvent(...))

    def update(self, ax):
        lims = ax.viewLim
        x_start, x_end = lims.intervalx
        if x_start < self.x_data[0]:
            x_start = self.x_data[0]
        if x_end > self.x_data[len(self.x_data) - 1]:
            x_end = self.x_data[len(self.x_data) - 1]
        idx_of_min, idx_of_max = (np.abs(self.x_data - x_start)).argmin(), (np.abs(self.x_data - x_end)).argmin()
        # print("during update: " + str(x.size))
        self.compute(idx_of_min, idx_of_max)

    def compute(self, idx_of_min, idx_of_max):
        self.idx_of_min = idx_of_min
        self.idx_of_max = idx_of_max
        with ThreadPoolExecutor() as executor:
            start = time.time()
            for f, l in zip(executor.map(self.simplify, self.lines), self.lines):
                l.line.set_data(f)
            end = time.time()
            print("total time: " + str(end - start))
            # executor.shutdown()
        # print("now drawing")
        for line in self.lines:
            line.line.axes.figure.canvas.draw_idle()
