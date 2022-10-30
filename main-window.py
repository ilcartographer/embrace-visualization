import os
from tkinter import *
from tkinter import filedialog
import datamodel
from datamodel import DataModel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from timeseries import TimeSeries

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

        # TODO get scrollbar working to be able to see all graphs
        vertical_scrollbar = Scrollbar(self)
        vertical_scrollbar.pack(side='right', fill='y')

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
        form_window.geometry("500x150")
        LoadDataForm(form_window, self.frames[GraphPage], self)

    # def slave_plot(self,time,ind):
    #     # Data points being put into the graph, update this to fill with the values in the Excel sheet
    #     #points_x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    #     #points_y1 = [3, 8, 1, 10, 15, 0, 0, 7, 9, 14, 20, 31, 5, 7, 19, 19, 35, 15, 20, 21]
    #     points_x1 = time
    #     points_y1 = ind
    #     # ***************************************************GRAPH 1*******************************************
    #     # the figure that will contain the plot
    #     fig_1 = Figure(figsize=(10, 2.5), dpi=100)
    #     # adding the subplot (I don't know exactly what a subplot does, but this defines the graph)
    #     plot1 = fig_1.add_subplot(111)
    #     # plotting graph 1
    #     plot1.plot(points_x1, points_y1)
    #     # creating the Tkinter canvas which houses the graphs
    #     canvas_1 = FigureCanvasTkAgg(fig_1, master=self)
    #     return canvas_1


    # def plot(self,time_axis,ind1,ind2,ind3):
    #     # Data points being put into the graph, update this to fill with the values in the Excel sheet

    #     points_x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    #     points_y1 = [3, 8, 1, 10, 15, 0, 0, 7, 9, 14, 20, 31, 5, 7, 19, 19, 35, 15, 20, 21]
    #     # ***************************************************GRAPH 1*******************************************
    #     canvas_1 = self.slave_plot(time_axis,ind1)
    #     # placing the canvas on the Tkinter window
    #     canvas_1.draw()
    #     canvas_1.get_tk_widget().pack()

    #     # ***************************************************GRAPH 2*******************************************
    #     canvas_2 = self.slave_plot(time_axis,ind2)
    #     canvas_2.draw()
    #     canvas_2.get_tk_widget().pack()

    #     # ***************************************************GRAPH 3*******************************************
    #     canvas_3 = self.slave_plot(time_axis,ind3)
    #     canvas_3.draw()
    #     canvas_3.get_tk_widget().pack()


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
        self.dm = graph_page.dm
        self.selected_dir = StringVar()

        # Create an Entry Widget in the Toplevel window
        entry = Entry(top, width=25, textvariable=self.selected_dir)
        entry.pack(fill='x')

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
        self.update_patients(self.selected_date.get())

    def on_date_change(self, value):
        self.selected_date.set(value)
        self.update_patients(value)

    def update_patients(self, date):
        local_dir = self.selected_dir.get() + "/" + date  # string file path calculation

        available_patients = [filename for filename in os.listdir(local_dir) if os.path.isdir(local_dir)]

        self.update_option_menu(self.patient_om, available_patients, self.on_patient_change)
        self.selected_patient.set(available_patients[0])
        # TODO: Add option for each directory in the currently selected date directory (similar to above)
        #   Directory to search should be self.selected_dir.get() + self.selected_date.get()
        # print("Update patients options")

    def on_patient_change(self, value):
        self.selected_patient.set(value)

    def update_option_menu(self, om, options, callback):
        menu = om["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string,
                             command=lambda value=string: callback(value))

    def submit(self, data):
        # self.submit_load_action(data.get())
        # change path to work with your computer
        self.submit_load_action(self.selected_dir.get()+"/"+self.selected_date.get()+"/"+self.selected_patient.get()+"/summary.csv")
        self.show_time_series_builder()
        self.master.destroy()

    def show_time_series_builder(self):
        time_series_window = Toplevel()
        TimeSeriesBuilder(time_series_window, self.get_column_names(), self.main_window, self.dm)


class TimeSeriesBuilder:
    def __init__(self, window, column_names, main_window, dm):
        self.master = window
        self.invalid_series = 'time'
        self.column_names = filter(self.filter_callback, column_names)
        self.main_window = main_window
        self.dm = dm
        self.add_widgets()

    def filter_callback(self, name):
        if (self.invalid_series not in name.lower()):
            return True
        else: 
            return False


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
        right_arrow_photo = PhotoImage(file='images/right_arrow.png')

        # store extra reference to photo so gc doesn't clear
        gc_right_label = Label(image=right_arrow_photo)
        gc_right_label.image = right_arrow_photo

        right_arrow_button = Button(second_frame_horizontal, height=20, width=40, image=right_arrow_photo,
                                    command=lambda: self.move_selections(lb_available, self.lb_selected))
        right_arrow_button.pack(side='top', anchor='n')
        left_arrow_photo = PhotoImage(file='images/left_arrow.png')

        # store extra reference to photo so gc doesn't clear
        gc_left_label = Label(image=left_arrow_photo)
        gc_left_label.image = left_arrow_photo

        left_arrow_button = Button(second_frame_horizontal, height=20, width=40, image=left_arrow_photo,
                                   command=lambda: self.move_selections(self.lb_selected, lb_available))
        left_arrow_button.pack(side='bottom', anchor='s')
        second_frame_horizontal.pack(side='left')
        self.lb_selected = Listbox(second_frame_vertical, selectmode='multiple')
        self.lb_selected.pack(side='right', anchor='e')
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

        selected_time_series_names = []
        cur_index = 0
        while cur_index < self.lb_selected.size():
            selected_time_series_names.append(self.lb_selected.get(cur_index))
            cur_index += 1 

        time_series = TimeSeries(self.main_window, self.dm)
        time_series.plot_selected_group(selected_time_series_names)
        self.main_window.time_series = time_series
        #self.main_window.add_time_series_builder_command()
        self.master.destroy()


app = MainWindow()
app.geometry("1000x1000")
app.mainloop()
