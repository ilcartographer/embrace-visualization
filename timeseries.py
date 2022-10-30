import os
from tkinter import *
from tkinter import filedialog
import datamodel
from datamodel import DataModel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)

class TimeSeries:
    def __init__(self, main_window, dm):
        self.main_window = main_window
        self.dm = dm
        #self.selected_time_series_names = selected_time_series_names
        self.canvases = []

    def add_plot(self,time, series_name, ind):
        points_x1 = time
        points_y1 = ind
        # the figure that will contain the plot
        fig_1 = Figure(figsize=(10, 2.5), dpi=100)
        # adding the subplot (I don't know exactly what a subplot does, but this defines the graph)
        plot1 = fig_1.add_subplot(111)
        # plotting graph 1
        plot1.plot(points_x1, points_y1)
        # creating the Tkinter canvas which houses the graphs
        canvas = FigureCanvasTkAgg(fig_1, master=self.main_window)
        # appending canvas info to the canvases list so they can be destroyed later
        self.canvases.append([
            {
                "label": series_name,
                "canvas": canvas
            }])
        plot_label = Label(self.main_window, text=series_name, font=LARGE_FONT)
        plot_label.pack()
        canvas.draw()
        canvas.get_tk_widget().pack()


    def plot_selected_group(self, selected_time_series_names):
        self.remove_all_plots()
        time_axis = self.dm.getcolumnaslist(0)

        for name in selected_time_series_names:
            ind = self.dm.getcolumnaslist(name)
            self.add_plot(time_axis, name, ind)
    
    def remove_all_plots(self):
        # TODO get this method to work correctly. It is not deleting the canvases currently
        for plot in self.canvases:
            plot["canvas"].get_tk_widget().delete('all')
            
        self.canvases.clear()
    
        