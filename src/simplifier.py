import math

import numpy as np


class Simplifier:
    def __init__(self, xdata, ydata):
        self.line = None
        self.origYData = ydata
        self.origXData = xdata
        self.pixels = 4096 * 2

    def simplify(self, x_start, x_end):
        # print("simplifying plot")
        idx_of_min, idx_of_max = (np.abs(self.origXData - x_start)).argmin(), (np.abs(self.origXData - x_end)).argmin()
        x = self.origXData[idx_of_min: idx_of_max]
        # print(x[0], x[len(x) - 1])
        y = self.origYData[idx_of_min: idx_of_max]
        # print(x.size, y.size)
        factor = math.floor(y.size / self.pixels)
        # print(factor)
        y = y[:factor * self.pixels]
        # print("number: " + str(factor * self.pixels))
        y = np.reshape(y, (self.pixels, factor))
        # find min and max
        # put min and max together
        # transpose matrix
        # reshape to one dimension
        y = np.reshape(np.transpose(np.vstack((y.min(1), y.max(1)))), self.pixels * 2)
        x = x[:: factor // 2]
        # print(x.size, y.size)
        return x[:self.pixels * 2], y

    def update(self, ax):
        # print("updating")
        # Update the line
        lims = ax.viewLim
        x_start, x_end = lims.intervalx
        # print(x_start, x_end)
        # get x and y 
        if x_start < self.origXData[0]:
            x_start = self.origXData[0]
        if x_end > self.origXData[len(self.origXData) - 1]:
            x_end = self.origXData[len(self.origXData) - 1]
        idx_of_min, idx_of_max = (np.abs(self.origXData - x_start)).argmin(), (np.abs(self.origXData - x_end)).argmin()
        x = self.origXData[idx_of_min: idx_of_max]
        # print("during update: " + str(x.size))
        if x.size < self.pixels or math.floor(x.size / self.pixels) / 2 < 1:
            # print("shortcut")
            y = self.origYData[idx_of_min: idx_of_max]
            self.line.set_data(x, y)
        else:
            self.line.set_data(*self.simplify(x_start, x_end))
        ax.figure.canvas.draw_idle()
