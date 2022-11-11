from tkinter import *
from tkinter import *

from RangeSlider import RangeSliderH
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

from dataset import AggregatedDataSet

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)


class TimeSeries:
    def __init__(self, parent, dm):
        self.parent = parent
        self.dm = dm
        self.canvases = []
        self.rs1 = None

    def add_plot(self, time, feature, order):
        self.canvases.append([
            {
                "label": feature,
                "canvas": AggregatedDataSet(self.parent, self.dm.getdatasetforfeature(time, feature), order).render()
            }])

    def plot_selected_group(self, selected_time_series_names):
        if self.rs1 is not None:
            self.rs1.grid_forget()

        min_time = DoubleVar()  # left handle variable
        max_time = DoubleVar()  # right handle variable

        # TODO: min/max value needs to come from dataset
        self.rs1 = RangeSliderH(self.parent, [min_time, max_time], padX=12, min_val=20, max_val=50, digit_precision='.0f')  # horizontal
        self.rs1.grid(row=1, column=0)  # or grid or place method could be used

        self.remove_all_plots()

        counter = 1
        for name in selected_time_series_names:
            counter += 1
            self.add_plot(0, name, counter)

    def remove_all_plots(self):
        for plot in self.canvases:
            plot[0]["canvas"].get_tk_widget().destroy()

        self.canvases.clear()
