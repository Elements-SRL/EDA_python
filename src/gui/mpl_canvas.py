from typing import List
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.widgets import RangeSlider


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.func = None
        self.slider: RangeSlider | None = None
        self.fig: Figure = plt.figure()
        self.ax1 = plt.subplot(211)
        self.ax2 = plt.subplot(212, sharex=self.ax1)
        self.ax1.callbacks.connect("xlim_changed", self.on_x_lims_change)
        self.ax2.callbacks.connect("xlim_changed", self.on_x_lims_change)
        self.slider_ax = self.fig.add_axes([0.1, 0, 0.8, 0.03])
        self.only_one_ax = plt.subplot(111)
        self.active_axis = [self.ax1, self.ax2]
        super(MplCanvas, self).__init__(self.fig)

    def set_one_plot(self):
        if self.only_one_ax not in self.fig.axes:
            self.fig.delaxes(self.ax1)
            self.fig.delaxes(self.ax2)
            self.only_one_ax = plt.subplot(111)
            self.only_one_ax.set_autoscale_on(False)  # Otherwise, infinite loop
            # TODO maybe this stuff is useless
            self.only_one_ax.callbacks.connect("xlim_changed", self.on_x_lims_change)
        self.active_axis = [self.only_one_ax]

    def set_two_plots(self):
        if self.only_one_ax in self.fig.axes:
            self.fig.delaxes(self.only_one_ax)
            self.ax1 = plt.subplot(211)
            self.ax2 = plt.subplot(212, sharex=self.ax1)
            self.ax1.callbacks.connect("xlim_changed", self.on_x_lims_change)
            self.ax2.callbacks.connect("xlim_changed", self.on_x_lims_change)
            self.active_axis = [self.ax1, self.ax2]
            self.ax1.set_autoscale_on(False)  # Otherwise, infinite loop
            self.ax2.set_autoscale_on(False)  # Otherwise, infinite loop
        # TODO maybe this stuff is useless
        if self.ax1 is not None and self.ax2 is not None:
            self.ax1.callbacks.connect("xlim_changed", self.on_x_lims_change)
            self.ax2.callbacks.connect("xlim_changed", self.on_x_lims_change)
            self.active_axis = [self.ax1, self.ax2]

    def get_active_axis(self) -> List[Axes]:
        return self.active_axis

    def clean_slider(self):
        self.fig.delaxes(self.slider_ax)
        self.slider_ax = self.fig.add_axes([0.1, 0, 0.8, 0.03])
        if self.slider is not None:
            self.slider.reset()

    def on_x_lims_change(self, event_ax):
        self.clean_slider()
        x_min, x_max = event_ax.get_xlim()
        self.slider = RangeSlider(self.slider_ax, "Range selector", x_min, x_max)
        self.slider.on_changed(self.func)

    def set_func(self, func):
        self.func = func

