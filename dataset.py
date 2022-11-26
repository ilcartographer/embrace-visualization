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


class AggregatedDataSet:
    def __init__(self, master, dataset, order, minx, maxx):
        self.master = master
        self.dataset = dataset
        self.order = order
        self.minx = minx
        self.maxx = maxx

    def set_bounds(self, minx, maxx):
        self.minx = minx
        self.maxx = maxx

    def render(self):
        filtered_points = [point for point in self.dataset.points if (point.x >= self.minx) & (point.x <= self.maxx)]
        points_x = [point.x for point in filtered_points]
        points_y = [point.y for point in filtered_points]

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
        canvas.get_tk_widget().grid(row=self.order, column=0, columnspan=3)

        return canvas
