from tkinter import *

from RangeSlider import RangeSliderH

from dataset import AggregatedDataSet

from datetime import datetime

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)


class TimeSeries:
    def __init__(self, parent, dm):
        self.parent = parent
        self.dm = dm
        self.canvases = []
        self.rs1 = None
        self.start_time = DoubleVar()
        self.start_time_str = StringVar()
        self.start_time.trace_add('write', self.update_labels)

        self.end_time_label = None
        self.end_time = DoubleVar()
        self.end_time_str = StringVar()

        start_time_label = Label(self.parent, textvariable=self.start_time_str)
        start_time_label.grid(row=1, column=0)

        end_time_label = Label(self.parent, textvariable=self.end_time_str)
        end_time_label.grid(row=1, column=2)

        update_btn = Button(parent, text="Update graphs", command=lambda: self.zoom_plots())
        update_btn.grid(row=2, column=1)

    def update_labels(self, *args):
        # TODO: Can do if/else for UTC/local time here. fromtimestamp() will do local, utcfromtimestamp() will do UTC.
        start_datetime = datetime.fromtimestamp(int(self.start_time.get()) / 1000).replace(microsecond=0)
        end_datetime = datetime.fromtimestamp(int(self.end_time.get()) / 1000).replace(microsecond=0)

        self.start_time_str.set(str(start_datetime))
        self.end_time_str.set(str(end_datetime))

    def add_plot(self, time, feature, order):
        data_set = AggregatedDataSet(self.parent, self.dm.getdatasetforfeature(time, feature), order,
                                     self.start_time.get(), self.end_time.get())
        self.add_plot_from_data_set(data_set)

    def add_plot_from_data_set(self, data_set):
        self.canvases.append(
            {
                "label": data_set.dataset.label,
                "data_set": data_set,
                "canvas": data_set.render()
            })

    def zoom_plots(self):
        data_sets = [canvas["data_set"] for canvas in self.canvases]

        self.remove_all_plots()

        for ds in data_sets:
            ds.set_bounds(self.start_time.get(), self.end_time.get())
            self.add_plot_from_data_set(ds)

    def plot_selected_group(self, selected_time_series_names):
        if self.rs1 is not None:
            self.rs1.grid_forget()

        time_values = self.dm.getcolumnaslist(2)  # 3rd column is the UTC timestamp
        min_value = min(time_values)
        max_value = max(time_values)

        self.start_time.set(min_value)
        self.end_time.set(max_value)

        self.rs1 = RangeSliderH(self.parent, [self.start_time, self.end_time], padX=110,
                                min_val=min_value, max_val=max_value, digit_precision='.0f', show_value=False)

        self.rs1.grid(row=1, column=1)  # or grid or place method could be used

        self.remove_all_plots()

        counter = 2
        for name in selected_time_series_names:
            counter += 1
            self.add_plot(2, name, counter)

    def remove_all_plots(self):
        for plot in self.canvases:
            plot["canvas"].get_tk_widget().destroy()

        self.canvases.clear()
