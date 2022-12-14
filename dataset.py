import datetime
from enum import Enum
from tkinter import *

import pandas as pd
import numpy as np
import scipy.stats
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import num2date
from matplotlib.figure import Figure
from mplcursors import cursor


class Interval(Enum):
    ONE_MINUTE = 1
    TWO_MINUTES = 2
    THIRTY_MINUTES = 3
    ONE_HOUR = 4
    THREE_HOURS = 5
    SIX_HOURS = 6
    ONE_DAY = 7


class Metric(Enum):
    MIN = 1
    MAX = 2
    AVG = 3
    SUM = 4
    MEDIAN = 5
    VARIANCE = 6
    STD = 7


class DataPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class DataSet:
    def __init__(self, label, points):
        self.points = points
        self.label = label

    def getxvalues(self):
        return [point.x for point in self.points]

    def getyvalues(self):
        return [point.y for point in self.points]


def listtodatetime(dates, dateortime, ):  # takes the date or time part of the strings in the array
    n = len(dates)
    labellist = [''] * n
    if dateortime == "date":
        for i in range(0, n):
            labellist[i] = (dates[i])[6:10]
    if dateortime == "time":
        for i in range(0, n):
            labellist[i] = (dates[i])[11:19]
    return labellist


class AggregatedDataSet:
    def __init__(self, master, dataset, order, interval, metric, minx, maxx, is_local_time):
        self.master = master
        self.dataset = dataset
        self.order = order
        self.aggregationSettings = AggregationSettings(interval, metric)
        self.minx = minx
        self.maxx = maxx
        self.is_local_time = is_local_time

    def update_settings(self, minx, maxx, is_local_time):
        self.minx = minx
        self.maxx = maxx
        self.is_local_time = is_local_time

    def render(self):
        points_x = self.dataset.getxvalues()
        points_y = self.dataset.getyvalues()

        # the figure that will contain the plot
        figure = Figure(figsize=(8, 2.5), dpi=100)
        figure.suptitle(self.dataset.label)

        # adding the subplot
        plot = figure.add_subplot(111)

        d = {'Datetime (UTC)': points_x, self.dataset.label: points_y}
        df = pd.DataFrame(data=d)
        df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'], utc=True)

        min_dt = pd.to_datetime(self.minx, unit='ms', utc=True)
        max_dt = pd.to_datetime(self.maxx, unit='ms', utc=True)

        df = df[(df['Datetime (UTC)'] >= min_dt) & (df['Datetime (UTC)'] <= max_dt)]

        the_plot = None

        if self.aggregationSettings.interval is not None and self.aggregationSettings.metric is not None:
            interval_rule = self.get_interval_string(self.aggregationSettings.interval).replace(" ", "")
            df_resampled = df.resample(rule=interval_rule, on='Datetime (UTC)')
            df_resampled_metric = self.match_metric(df_resampled, self.aggregationSettings.metric.name)
            the_plot = df_resampled_metric.plot(ax=plot)
        else:
            the_plot = df.plot(x="Datetime (UTC)", ax=plot)

        the_cursor = cursor(the_plot, hover=True)
        the_cursor.connect(
            "add", lambda sel: self.set_annotation(sel))

        # remove the x ticks for now, this is causing huge performance issues
        # TODO: future state, maybe we can add a small number of ticks
        figure.gca().get_xaxis().set_ticks([])
        # creating the Tkinter canvas which houses the graphs
        canvas = FigureCanvasTkAgg(figure, self.master.interior)
        canvas.draw()
        canvas.get_tk_widget().grid(row=self.order, column=0, columnspan=3)
        # canvas.get_tk_widget().pack()
        self.enable_settings_menu(canvas)

        return canvas

    def set_annotation(self, sel):
        date_text = num2date(sel.target[0], datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo) if \
            self.is_local_time is True else num2date(sel.target[0])
        text = "x: {}\ny: {}".format(date_text, sel.target[1])
        sel.annotation.set_text(text)

    def enable_settings_menu(self, canvas):
        settings_menu = Menu(self.master.interior, tearoff=0)
        agg_sub_menu = Menu(settings_menu, tearoff=0)

        interval_sub_menu = Menu(agg_sub_menu, tearoff=0)
        for variant in iter(Interval):
            variant_name = Enum.__getattribute__(Interval, variant.name)
            interval_sub_menu.add_command(
                label=self.get_interval_string(variant),
                command=lambda name=variant_name: self.update_agg_settings("interval", name)
            )

        metric_sub_menu = Menu(agg_sub_menu, tearoff=0)
        for variant in iter(Metric):
            variant_name = Enum.__getattribute__(Metric, variant.name)
            metric_sub_menu.add_command(
                label=variant.name,
                command=lambda name=variant_name: self.update_agg_settings("metric", name)
            )

        agg_sub_menu.add_cascade(
            label="Interval",
            menu=interval_sub_menu
        )
        agg_sub_menu.add_cascade(
            label="Metric",
            menu=metric_sub_menu
        )
        settings_menu.add_cascade(
            label="Aggregate",
            menu=agg_sub_menu
        )
        settings_menu.add_command(label="Describe", command=lambda: self.display_summary())

        canvas.get_tk_widget().bind("<Button-3>", lambda event: self.handle_rightclick(event, menu=settings_menu))

    def handle_rightclick(self, e, menu):
        try:
            menu.tk_popup(e.x_root, e.y_root)
        finally:
            menu.grab_release()

    def display_summary(self):
        points_y = self.dataset.getyvalues()
        num_array = np.array(points_y)
        stats = {
            'count': len(points_y),
            'mean': np.mean(num_array),
            'std': np.std(num_array),
            'min': np.amin(num_array),
            'max': np.amax(num_array),
            'twoTenths': np.percentile(num_array, .2),
            'twoFive': np.percentile(num_array, 2.5),
            'twentyFive': np.percentile(num_array, 25),
            'fifty': np.percentile(num_array, 50),
            'seventyFive': np.percentile(num_array, 75),
            'ninetySevenFive': np.percentile(num_array, 97.5),
            'ninetyNineNine': np.percentile(num_array, 99.9),
            'kurtosis': scipy.stats.kurtosis(num_array),
            'skewness': scipy.stats.skew(num_array)
        }

        display = Toplevel(self.master)
        self.build_stats_window(display, stats)
        print(stats)

    @staticmethod
    def build_stats_window(window, stats):
        Label(window, text='Count: {}'.format(stats['count'])).grid(row=0, column=0, sticky='w')
        Label(window, text='Mean: {}'.format(stats['mean'])).grid(row=1, column=0, sticky='w')
        Label(window, text='Std: {}'.format(stats['std'])).grid(row=2, column=0, sticky='w')
        Label(window, text='Min: {}'.format(stats['min'])).grid(row=3, column=0, sticky='w')
        Label(window, text='Max: {}'.format(stats['max'])).grid(row=4, column=0, sticky='w')
        Label(window, text='Kurtosis: {}'.format(stats['kurtosis'])).grid(row=5, column=0, sticky='w')
        Label(window, text='Skewness: {}'.format(stats['skewness'])).grid(row=6, column=0, sticky='w')
        Label(window, text='.2%: {}'.format(stats['twoTenths'])).grid(row=0, column=1, sticky='w')
        Label(window, text='2.5%: {}'.format(stats['twoFive'])).grid(row=1, column=1, sticky='w')
        Label(window, text='25%: {}'.format(stats['twentyFive'])).grid(row=2, column=1, sticky='w')
        Label(window, text='50%: {}'.format(stats['fifty'])).grid(row=3, column=1, sticky='w')
        Label(window, text='75%: {}'.format(stats['seventyFive'])).grid(row=4, column=1, sticky='w')
        Label(window, text='97.5%: {}'.format(stats['ninetySevenFive'])).grid(row=5, column=1, sticky='w')
        Label(window, text='99.9%: {}'.format(stats['ninetyNineNine'])).grid(row=6, column=1, sticky='w')

    @staticmethod
    def get_interval_string(variant):
        match variant.name:
            case "ONE_MINUTE":
                return "1 min"
            case "TWO_MINUTES":
                return "2 min"
            case "THIRTY_MINUTES":
                return "30 min"
            case "ONE_HOUR":
                return "1 h"
            case "THREE_HOURS":
                return "3 h"
            case "SIX_HOURS":
                return "6 h"
            case "ONE_DAY":
                return "1 d"

    def match_metric(self, df, variant):
        match variant:
            case "MIN":
                return df[self.dataset.label].min()
            case "MAX":
                return df[self.dataset.label].max()
            case "AVG":
                return df.mean()
            case "SUM":
                return df.sum()
            case "MEDIAN":
                return df.median()
            case "VARIANCE":
                return df.var(ddof=0)
            case "STD":
                return df.std(ddof=0)

    def update_agg_settings(self, setting_type, setting_value):
        if setting_type == "interval":
            metric_setting = Metric.MIN
            if self.aggregationSettings.metric is not None:
                metric_setting = self.aggregationSettings.metric
            self.master.time_series.plot_selected_group(setting_value, metric_setting)
        elif setting_type == "metric":
            # interval_setting = Interval.ONE_MINUTE
            interval_setting = Interval.TWO_MINUTES
            if self.aggregationSettings.interval is not None:
                interval_setting = self.aggregationSettings.interval
            self.master.time_series.plot_selected_group(interval_setting, setting_value)


class AggregationSettings:
    def __init__(self, interval, metric):
        self.interval = interval
        self.metric = metric
