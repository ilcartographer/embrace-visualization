from tkinter import *
from tkinter import filedialog
import datamodel
from datamodel import datamodel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
LARGE_FONT = ("Verdana", 12)


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
        print("show_load_data")
        form_window = Toplevel(self)
        LoadDataForm(form_window, self.frames[GraphPage].load_data)

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
        self.disp = StringVar()#still required, currently works as display placeholder,
        self.dm = datamodel(self.disp)#holds the actual data
        self.disp.set(self.dm)#displays dm
        self.controller = controller

        label = Label(self, text="This is the graph page", font=LARGE_FONT)

        label.pack(pady=10, padx=10)

        data_label = Label(self, textvariable=self.disp, font=LARGE_FONT)
        data_label.pack(pady=10, padx=10)



    def load_data(self, filename):#updates dm, disp
        self.dm.setnewurl(filename)
        self.disp.set(self.dm)

        self.controller.plot() #Creates the graphs when the "OK" button is clicked in Load Data

class LoadDataForm:
    def __init__(self, top, load_action):
        self.master = top
        self.submit_load_action = load_action

        self.selected_path = StringVar()

        # Create an Entry Widget in the Toplevel window
        entry = Entry(top, width=25, textvariable=self.selected_path)
        entry.pack()

        load_button = Button(top, text="Select file...", command=lambda: self.select_file())
        load_button.pack() # TODO: How to do this side-by-side with the label?
        # Create a Button Widget in the Toplevel Window
        button = Button(top, text="Ok", command=lambda: self.submit(entry))
        button.pack(pady=5, side=TOP)

    def select_file(self):
        self.selected_path.set(filedialog.askopenfilename(initialdir="./", title="Select file",
                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*"))))

    def submit(self, data):
        self.submit_load_action(data.get())
        self.master.destroy()


app = MainWindow()
app.mainloop()
