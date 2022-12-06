import os
import pandas as pd
from tkinter import *
from tkinter import filedialog


from datamodel import DataModel
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


class GraphPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.disp = StringVar()  # still required, currently works as display placeholder,
        self.dm = DataModel(self.disp)  # holds the actual data
        self.controller = controller
        self.time_series = None

        ###############
        # The following section sets up the scrollable frame. Based on the solution from
        # https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame/16198198#16198198
        # TODO: As in the example, maybe make a ScrollableFrame class and have GraphPage extend it?
        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)

        ###############
        top_frame = Frame(interior)

        label = Label(top_frame, text="This is the graph page", font=LARGE_FONT)
        label.pack(side='left')
        self.reset_agg_setting_button = Button(top_frame, text="Reset", command=lambda: self.time_series.plot_selected_group(None, None))
        self.metric_setting_label = Label(top_frame, text='Metric: None', font=SMALL_FONT)

        self.interval_setting_label = Label(top_frame, text='Interval: None', font=SMALL_FONT)
        top_frame.pack(fill='x')

        self.timezone = StringVar()
        self.timezone.set("Time Zone: NONE")

        time_zone = Label(top_frame, textvariable= self.timezone, font=LARGE_FONT)
        time_zone.pack(side='top')

        # Note: Leaving this here for now to mess with different figure settings more efficiently
        # f = Figure(figsize=(5, 5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
        #
        # f.gca().get_xaxis().set_ticks([])
        # f.gca().get_yaxis().set_ticks([])
        # canvas = FigureCanvasTkAgg(f, self)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    def load_data(self, filename):  # updates dm, disp
        self.dm.setnewurl(filename)
        self.disp.set(self.dm)

        self.timezone.set("Time Zone: " + str(self.dm.getcolumnaslist("Timezone (minutes)")[1]))
        time_zone = Label(textvariable= self.timezone, font=LARGE_FONT)
        time_zone.pack(side='top')

        # self.controller.plot()  # Creates the graphs when the "OK" button is clicked in Load Data


class LoadDataForm:
    def __init__(self, top, graph_page, main_window):
        self.master = top
        self.submit_load_action = graph_page.load_data
        self.get_column_names = graph_page.dm.getcolumnnameslist
        self.graph_page = graph_page
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
        button = Button(top, text="Ok", command=lambda: self.submit())
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

    def submit(self):
        # self.submit_load_action(data.get())
        # change path to work with your computer
        self.submit_load_action(
            self.selected_dir.get() + "/" + self.selected_date.get() + "/" + self.selected_patient.get() + "/summary.csv")
        self.show_time_series_builder()
        self.master.destroy()

    def show_time_series_builder(self):
        time_series_window = Toplevel()
        TimeSeriesBuilder(time_series_window, self.get_column_names(), self.graph_page, self.dm)


class TimeSeriesBuilder:
    def __init__(self, window, column_names, graph_page, dm):
        self.master = window
        self.invalid_series = 'time'
        self.column_names = filter(self.filter_callback, column_names)
        self.graph_page = graph_page
        self.dm = dm
        self.add_widgets()

        if self.graph_page.time_series is None:
            self.time_series = TimeSeries(self.graph_page, self.dm)
            self.graph_page.time_series = self.time_series
        else:
            self.time_series = graph_page.time_series

    def filter_callback(self, name):
        return self.invalid_series not in name.lower()

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
        finish_button = Button(third_frame_vertical, text="Finish", command=lambda: self.submit())
        finish_button.pack(side='right')
        third_frame_vertical.pack(fill='x')

    def move_selections(self, lb_origin, lb_destination):
        for option_index in lb_origin.curselection():
            lb_destination.insert(option_index, lb_origin.get(option_index))

        for option_index in reversed(lb_origin.curselection()):
            lb_origin.delete(option_index)

    def submit(self):
        selected_time_series_names = []
        cur_index = 0
        while cur_index < self.lb_selected.size():
            selected_time_series_names.append(self.lb_selected.get(cur_index))
            cur_index += 1
        self.time_series.set_selected_time_series_names(selected_time_series_names)
        self.time_series.plot_selected_group(None, None)
        
        self.graph_page.reset_agg_setting_button.pack(side='right')
        self.graph_page.metric_setting_label.pack(side='right')
        self.graph_page.interval_setting_label.pack(side='right')

        self.master.destroy()

app = MainWindow()
app.geometry("1000x1000")
app.mainloop()
