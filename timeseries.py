from tkinter import *
from tkinter import *

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

    def add_plot(self, time, feature):
        self.canvases.append([
            {
                "label": feature,
                "canvas": AggregatedDataSet(self.parent, self.dm.getdatasetforfeature(time, feature)).render()
            }])

    def plot_selected_group(self, selected_time_series_names):
        self.remove_all_plots()

        for name in selected_time_series_names:
            self.add_plot(0, name)

    def remove_all_plots(self):
        # TODO get this method to work correctly. It is not deleting the canvases currently
        for plot in self.canvases:
            plot[0]["canvas"].get_tk_widget().destroy()

        self.canvases.clear()
