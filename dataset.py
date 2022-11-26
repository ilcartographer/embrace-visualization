from tkinter import BOTTOM, BOTH
from tkinter import Menu
from enum import Enum
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Interval(Enum):
    ONE_MINUTE = 1
    THIRTY_MINUTES = 2
    ONE_HOUR = 3
    THREE_HOURS = 4
    SIX_HOURS = 5
    ONE_DAY = 6
    

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


class AggregatedDataSet:
    def __init__(self, master, dataset, order, interval, metric):
        self.master = master
        self.dataset = dataset
        self.order = order
        self.aggregationSettings = self.assign_aggregation_settings(interval, metric)
        # lambda i = interval,  m = metric: AggregationSettings(i,m)

    def render(self):
        # def slave_plot(self, time, ind):
        points_x = self.dataset.getxvalues()
        points_y = self.dataset.getyvalues()

        # the figure that will contain the plot
        figure = Figure(figsize=(10, 2.5), dpi=100)
        figure.suptitle(self.dataset.label)

        # adding the subplot
        plot = figure.add_subplot(111)

        d = {'Datetime (UTC)': points_x, self.dataset.label: points_y}
        df = pd.DataFrame(data = d)
        if self.aggregationSettings.interval is not None and self.aggregationSettings.metric is not None:
            df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
            interval_rule = self.get_interval_string(self.aggregationSettings.interval.name).replace(" ", "")
            df_resampled= df.resample(rule = interval_rule, on='Datetime (UTC)')
            df_resampled_metric = self.match_metric(df_resampled, self.aggregationSettings.metric.name)
            df_resampled_metric.plot(ax=plot)
        else: 
            df.plot(ax=plot)
        # plotting graph 1
        # plot.plot(points_x, points_y)
        
        # remove the x ticks for now, this is causing huge performance issues
        # TODO: future state, maybe we can add a small number of ticks
        figure.gca().get_xaxis().set_ticks([])
        # creating the Tkinter canvas which houses the graphs
        canvas = FigureCanvasTkAgg(figure, self.master.interior)
        canvas.draw()
        canvas.get_tk_widget().grid(row=self.order, column=0)
        self.enable_settings_menu(canvas)
        return canvas

    def enable_settings_menu(self, canvas):
        settings_menu = Menu(self.master.interior, tearoff=0)
        agg_sub_menu = Menu(settings_menu, tearoff=0)

        interval_sub_menu = Menu(agg_sub_menu, tearoff=0)
        for variant in iter(Interval):
            variant_name = Enum.__getattribute__(Interval, variant.name)
            interval_sub_menu.add_command(
                label = self.get_interval_string(variant.name), 
                command=lambda name=variant_name: self.update_agg_settings("interval", name)
            )

        metric_sub_menu = Menu(agg_sub_menu, tearoff=0)
        for variant in iter(Metric):
            variant_name = Enum.__getattribute__(Metric, variant.name)
            metric_sub_menu.add_command(
                label = variant.name, 
                command=lambda name=variant_name: self.update_agg_settings("metric", name)
            )

        agg_sub_menu.add_cascade(
            label = "Interval",
            menu=interval_sub_menu
        )
        agg_sub_menu.add_cascade(
            label = "Metric",
            menu = metric_sub_menu     
        )
        settings_menu.add_cascade(
            label = "Aggregate",
            menu = agg_sub_menu
        )
        settings_menu.add_command(label="Describe")

        canvas.get_tk_widget().bind("<Button-3>", lambda event: self.handle_rightclick(event,menu=settings_menu))
    
    def handle_rightclick(self, e, menu):
        try:
            menu.tk_popup(e.x_root, e.y_root)
        finally:
            menu.grab_release()
    
    def get_interval_string(self, variant):
        match variant:
            case "ONE_MINUTE": 
                return "1 min"
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
                return df.min()
            case "MAX": 
                return df.max()
            case "AVG": 
                return df.mean()
            case "SUM": 
                return df.sum()
            case "MEDIAN":
                return df.median()
            case "VARIANCE": 
                return df.var()
            case "STD": 
                return df.std()

    def update_agg_settings(self, setting_type, setting_value):
            if setting_type == "interval":
                self.master.time_series.plot_selected_group(setting_value, self.aggregationSettings.metric)
            elif setting_type == "metric":
                self.master.time_series.plot_selected_group(self.aggregationSettings.interval, setting_value)

    def assign_aggregation_settings(self, interval, metric):
        if interval is not None and metric is not None:
            return AggregationSettings(interval, metric)
        elif interval is not None and metric is None:
            return AggregationSettings(interval, Metric.AVG)
        elif interval is None and metric is not None:
            return AggregationSettings(Interval.ONE_MINUTE, metric)
        else:
            return AggregationSettings(None, None)


class AggregationSettings:
    def __init__(self, interval, metric):
        self.interval = interval
        self.metric = metric