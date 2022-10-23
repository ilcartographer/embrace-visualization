import os
from tkinter import *
from tkinter import filedialog
import datamodel
from datamodel import DataModel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)


def client_exit():
    exit()


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.data_file = None
        self.frames = None
        self.init_window()

    def init_window(self):
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu = Menu(self)
        self.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Load data...", command=self.show_load_data)
        file.add_command(label="Exit", command=client_exit)

        menu.add_cascade(label="File", menu=file)

        self.frames = {}

        frame = GraphPage(container, self)
        self.frames[GraphPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GraphPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_load_data(self):
        form_window = Toplevel(self)
        LoadDataForm(form_window, self.frames[GraphPage], self)

    def plot(self):
        # Data points being put into the graph, update this to fill with the values in the Excel sheet
        points_x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        points_y1 = [3, 8, 1, 10, 15, 0, 0, 7, 9, 14, 20, 31, 5, 7, 19, 19, 35, 15, 20, 21]

        # ***************************************************GRAPH 1*******************************************
        # the figure that will contain the plot
        fig_1 = Figure(figsize=(10, 2.5), dpi=100)
        # adding the subplot (I don't know exactly what a subplot does, but this defines the graph)
        plot1 = fig_1.add_subplot(111)
        # plotting graph 1
        plot1.plot(points_x1, points_y1)
        # creating the Tkinter canvas which houses the graphs
        canvas_1 = FigureCanvasTkAgg(fig_1, master=self)
        canvas_1.draw()
        # placing the canvas on the Tkinter window
        canvas_1.get_tk_widget().pack()
        # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(canvas_1, window)
        # toolbar.update()
        # placing the toolbar on the Tkinter window
        # canvas_1.get_tk_widget().pack()

        # ***************************************************GRAPH 2*******************************************
        # the figure that will contain the plot
        fig_2 = Figure(figsize=(10, 2.5), dpi=100)
        # adding the subplot (I don't know exactly what a subplot does, but this defines the graph)
        plot2 = fig_2.add_subplot(111)
        # plotting graph 2
        plot2.plot(points_x1, points_y1)
        # creating the Tkinter canvas which houses the graphs
        canvas_2 = FigureCanvasTkAgg(fig_2, master=self)
        canvas_2.draw()
        # placing the canvas on the Tkinter window
        canvas_2.get_tk_widget().pack()
        # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(canvas_2, window)
        # toolbar.update()
        # placing the toolbar on the Tkinter window
        # canvas_2.get_tk_widget().pack()

        # ***************************************************GRAPH 3*******************************************
        # the figure that will contain the plot
        fig_3 = Figure(figsize=(10, 2.5), dpi=100)
        # adding the subplot (I don't know exactly what a subplot does, but this defines the graph)
        plot3 = fig_3.add_subplot(111)
        # plotting graph 2
        plot3.plot(points_x1, points_y1)
        # creating the Tkinter canvas which houses the graphs
        canvas_3 = FigureCanvasTkAgg(fig_3, master=self)
        canvas_3.draw()
        # placing the canvas on the Tkinter window
        canvas_3.get_tk_widget().pack()
        # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(canvas_3, window)
        # toolbar.update()
        # placing the toolbar on the Tkinter window
        # canvas_3.get_tk_widget().pack()


class GraphPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.disp = StringVar()  # still required, currently works as display placeholder,
        self.dm = DataModel(self.disp)  # holds the actual data
        self.disp.set(self.dm)  # displays dm
        self.controller = controller

        #label = Label(self, text="This is the graph page", font=LARGE_FONT)

        #label.pack(pady=10, padx=10)

        #data_label = Label(self, textvariable=self.disp, font=LARGE_FONT)
        #data_label.pack(pady=10, padx=10)

    def load_data(self, filename):  # updates dm, disp
        self.dm.setnewurl(filename)
        self.disp.set(self.dm)

        # self.controller.plot()  # Creates the graphs when the "OK" button is clicked in Load Data


class LoadDataForm:
    def __init__(self, top, graph_page, main_window):
        self.master = top
        self.submit_load_action = graph_page.load_data
        self.get_column_names = graph_page.dm.getcolumnnameslist
        self.main_window = main_window

        self.selected_dir = StringVar()

        # Create an Entry Widget in the Toplevel window
        entry = Entry(top, width=25, textvariable=self.selected_dir)
        entry.pack()

        load_button = Button(top, text="Select file...", command=lambda: self.select_file())
        load_button.pack()  # TODO: How to do this side-by-side with the label?

        self.selected_date = StringVar()
        self.selected_date.set("")

        self.date_om = OptionMenu(top, self.selected_date, *[""])
        self.date_om.pack()

        self.selected_patient = StringVar()
        self.patient_om = OptionMenu(top, self.selected_patient, *[""])
        self.patient_om.pack()

        # Create a Button Widget in the Toplevel Window
        button = Button(top, text="Ok", command=lambda: self.submit(entry))
        button.pack(pady=5, side=TOP)

    def select_file(self):
        data_dir = filedialog.askdirectory(initialdir="./", title="Select DataSet Directory...")
        self.selected_dir.set(data_dir)

        available_dates = [filename for filename in os.listdir(data_dir) if os.path.isdir(data_dir)]
        self.update_option_menu(self.date_om, available_dates, self.on_date_change)
        self.selected_date.set(available_dates[0])

    def on_date_change(self, value):
        self.selected_date.set(value)
        self.update_patients()

    def update_patients(self):

        # TODO: Add option for each directory in the currently selected date directory (similar to above)
        #   Directory to search should be self.selected_dir.get() + self.selected_date.get()
        print("Update patients options")

    def update_option_menu(self, om, options, callback):
        menu = om["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string,
                             command=lambda value=string: callback(value))

    def submit(self, data):
        # self.submit_load_action(data.get())
        # change path to work with your computer
        self.submit_load_action("Dataset/20200120/312/summary.csv")
        self.show_time_series_builder()
        self.master.destroy()

    def show_time_series_builder(self):
        time_series_window = Toplevel(height='1000', width='1000')
        TimeSeriesBuilder(time_series_window, self.get_column_names(), self.main_window)


class TimeSeriesBuilder:
    def __init__(self, window, column_names, main_window):
        self.master = window
        self.column_names = column_names
        self.main_window = main_window
        self.add_widgets()

    def add_widgets(self):
        first_frame_vertical = Frame(self.master)
        available_label = Label(first_frame_vertical, text="Available Series", font=SMALL_FONT)
        available_label.pack(side='left', anchor='w')
        selected_label = Label(first_frame_vertical, text="Selected Series", font=SMALL_FONT)
        selected_label.pack(side='right', anchor='e')
        first_frame_vertical.pack(side='top', fill='x')
        second_frame_vertical = Frame(self.master)
        lb_available = Listbox(second_frame_vertical, selectmode='multiple')
        for index, series_name in enumerate(self.column_names):
            lb_available.insert(index, series_name)
        lb_available.pack(side='left', anchor='w')
        second_frame_horizontal = Frame(second_frame_vertical)
        right_arrow_photo = PhotoImage(file='right_arrow.png')

        # store extra reference to photo so gc doesn't clear
        gc_right_label = Label(image=right_arrow_photo)
        gc_right_label.image = right_arrow_photo

        right_arrow_button = Button(second_frame_horizontal, height=20, width=40, image=right_arrow_photo,
                                    command=lambda: self.move_selections(lb_available, lb_selected))
        right_arrow_button.pack(side='top', anchor='n')
        left_arrow_photo = PhotoImage(file='left_arrow.png')

        # store extra reference to photo so gc doesn't clear
        gc_left_label = Label(image=left_arrow_photo)
        gc_left_label.image = left_arrow_photo

        left_arrow_button = Button(second_frame_horizontal, height=20, width=40, image=left_arrow_photo,
                                   command=lambda: self.move_selections(lb_selected, lb_available))
        left_arrow_button.pack(side='bottom', anchor='s')
        second_frame_horizontal.pack(side='left')
        lb_selected = Listbox(second_frame_vertical, selectmode='multiple')
        lb_selected.pack(side='right', anchor='e')
        second_frame_vertical.pack(fill='x')
        third_frame_vertical = Frame(self.master)
        finish_button = Button(third_frame_vertical, text="Finish", command=lambda: self.finish())
        finish_button.pack(side='right')
        third_frame_vertical.pack(fill='x')

    def move_selections(self, lb_origin, lb_destination):
        for option_index in lb_origin.curselection():
            lb_destination.insert(option_index, lb_origin.get(option_index))

        for option_index in reversed(lb_origin.curselection()):
            lb_origin.delete(option_index)

    def finish(self):
        self.main_window.plot()  # Creates the graphs when the "OK" button is clicked in Load Data
        self.master.destroy()


app = MainWindow()
app.mainloop()
