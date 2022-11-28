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
        self.interval = None
        self.metric = None
        self.selected_time_series_names = None

    def set_selected_time_series_names(self, value):
        self.selected_time_series_names = value

    def add_plot(self, time, feature, order):
        time_values = self.dm.getcolumnaslist(2)
        min_value = min(time_values)
        max_value = max(time_values)
        self.canvases.append([
            {
                "label": feature,
                "canvas": AggregatedDataSet(self.parent, self.dm.getdatasetforfeature(time, feature), order, self.interval, self.metric, min_value, max_value).render()
            }])

    def plot_selected_group(self, interval, metric):
        if self.rs1 is not None:
            # self.rs1.grid_forget()
            self.rs1.pack_forget()
        self.interval = interval
        self.metric = metric

        min_time = DoubleVar()  # left handle variable
        max_time = DoubleVar()  # right handle variable

        # TODO: min/max value needs to come from dataset
        self.rs1 = RangeSliderH(self.parent.interior, [min_time, max_time], padX=12, min_val=20, max_val=50, digit_precision='.0f')  # horizontal
        # self.rs1.grid(row=1, column=0)  # or grid or place method could be used
        self.rs1.pack()  

        self.remove_all_plots()

        if self.interval is None and self.metric is None:
            self.parent.interval_setting_label.config(text = 'Interval: None')
            self.parent.metric_setting_label.config(text = 'Metric: None')
        else:
            self.parent.interval_setting_label.config(text = 'Interval: ' + AggregatedDataSet.get_interval_string(self.interval))
            self.parent.metric_setting_label.config(text = 'Metric: ' + self.metric.name)
            
        counter = 2

        for name in self.selected_time_series_names:
            counter += 1
            self.add_plot(0, name, counter)

    def remove_all_plots(self):
        for plot in self.canvases:
            plot[0]["canvas"].get_tk_widget().destroy()

        self.canvases.clear()
