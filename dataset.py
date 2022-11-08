from tkinter import BOTTOM, BOTH

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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
    def __init__(self, master, dataset):
        self.master = master
        self.dataset = dataset

    def render(self):
        # def slave_plot(self, time, ind):
        points_x = self.dataset.getxvalues()
        points_y = self.dataset.getyvalues()

        # the figure that will contain the plot
        figure = Figure(figsize=(10, 2.5), dpi=100)
        figure.suptitle(self.dataset.label)

        # adding the subplot
        plot = figure.add_subplot(111)
        # plotting graph 1
        plot.plot(points_x, points_y)

        # remove the x ticks for now, this is causing huge performance issues
        # TODO: future state, maybe we can add a small number of ticks
        figure.gca().get_xaxis().set_ticks([])
        # creating the Tkinter canvas which houses the graphs
        canvas = FigureCanvasTkAgg(figure, self.master)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        return canvas