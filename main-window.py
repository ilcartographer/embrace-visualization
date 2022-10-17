from tkinter import *
from tkinter import filedialog

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


class GraphPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.data_filename = StringVar()
        label = Label(self, text="This is the graph page", font=LARGE_FONT)

        label.pack(pady=10, padx=10)

        data_label = Label(self, textvariable=self.data_filename, font=LARGE_FONT)
        data_label.pack(pady=10, padx=10)

    def load_data(self, filename):
        self.data_filename.set(filename)


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
