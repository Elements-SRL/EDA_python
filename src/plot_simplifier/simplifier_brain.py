from concurrent.futures import ThreadPoolExecutor
import math
from typing import List, Tuple
import numpy as np
from numpy import ndarray
from src.plot_simplifier.line import Line


def _get_range(y_ranges: List[Tuple[float, float]]):
    y_min_global, y_max_global = y_ranges[0]
    for y_min, y_max in y_ranges:
        if y_min < y_min_global:
            y_min_global = y_min
        if y_max > y_max_global:
            y_max_global = y_max
    return y_min_global, y_max_global


class SimplifierBrain:

    def __init__(self, xdata: ndarray, lines: List[Line]):
        self.idx_of_max = None
        self.idx_of_min = None
        self.lines = lines
        self.x_data = xdata
        self.pixels = 4096 * 2

    def setup(self) -> Tuple[Tuple[float, float], List[Tuple[float, float]]]:
        self.compute(idx_of_min=0, idx_of_max=self.x_data.size - 1)
        x_range = (self.x_data.min(), self.x_data.max())
        axis = sorted({line.axis for line in self.lines})
        y_ranges_to_ret = []
        for ax in axis:
            y_ranges = [(line.y.min(), line.y.max()) for line in self.lines if line.axis == ax]
            y_ranges_to_ret.append(_get_range(y_ranges))
        return x_range, y_ranges_to_ret

    def simplify(self, line: Line):
        last_x = self.x_data[self.idx_of_max]
        first_x = self.x_data[self.idx_of_min]
        y = line.y[self.idx_of_min: self.idx_of_max]
        if y.size < self.pixels:
            return np.linspace(first_x, last_x, y.size), y
        factor = math.floor(y.size / self.pixels)
        y1 = y[:factor * self.pixels]
        y2 = y[factor * self.pixels:]
        y = np.reshape(y1, (self.pixels, factor))
        # find min and max
        # put min and max together
        # transpose matrix
        # reshape to one dimension
        y = np.append(np.reshape(np.transpose(np.vstack((y.min(1), y.max(1)))), self.pixels * 2), [y2.min(), y2.max()])
        # end = time.time()
        # print(end - start)
        return np.linspace(first_x, last_x, y.size), y

    def update(self, ax):
        lims = ax.viewLim
        x_start, x_end = lims.intervalx
        if x_start < self.x_data[0]:
            x_start = self.x_data[0]
        if x_end > self.x_data[len(self.x_data) - 1]:
            x_end = self.x_data[len(self.x_data) - 1]
        idx_of_min, idx_of_max = (np.abs(self.x_data - x_start)).argmin(), (np.abs(self.x_data - x_end)).argmin()
        self.compute(idx_of_min, idx_of_max)

    def compute(self, idx_of_min, idx_of_max):
        self.idx_of_min = idx_of_min
        self.idx_of_max = idx_of_max
        with ThreadPoolExecutor() as executor:
            # start = time.time()
            for f, l in zip(executor.map(self.simplify, self.lines), self.lines):
                l.line.set_data(f)
            # end = time.time()
            # print("total time: " + str(end - start))
        for line in self.lines:
            line.line.axes.figure.canvas.draw_idle()
