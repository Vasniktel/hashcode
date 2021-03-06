from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import *
from assets.simulator import Simulator
from assets.visualizer import Visualizer
import os

# tkinter - visual lib for python
# Simulator - class to simulate the process
# Visualizer - class for visualizing the results

class Window(Frame): # inherits from Frame
    def create_widgets(self):
        """Function to create widgets on main window.
        Creates: input file button, output file button, fields
        to these files; text field with content of input file;
        Proceed button."""

        # Button to determine file for output
        self.output = Button(self, text="Output", command=self.upload_output, width=22, height=1)
        self.output.grid(row=0, column=1, pady=(0,10))

        # Text field, that shows path to output file
        self.text_file_output = Entry(self, width=83)
        self.text_file_output.grid(row=0, column=2, pady=(0,5), padx=(5,5))

        # Button to upload input file
        self.input = Button(self, text="Input", command=self.upload_input, width=22, height=1)
        self.input.grid(row=1, column=1, pady=(0,10))

        # Text field, that shows path to input file
        self.text_file_input = Entry(self, width=83)
        self.text_file_input.grid(row=1, column=2, pady=(0,5), padx=(5,5))

        # Text field. Shows uploaded input file
        self.text = scrolledtext.ScrolledText(self, width=125, height=40, relief="sunken")
        self.grid(padx=20, pady=20)
        self.text.grid(row=2, column=1, columnspan=2)

        # Process button
        self.proceed = Button(self)
        self.proceed["text"] = "Process"
        self.proceed["command"] = self.process
        self.proceed["width"] = 30
        self.proceed.grid(row=3, column=1, pady=(14,0), columnspan=2)

    def __init__(self, master=None):
        """ Initializing function. Setting the width, height window parameters.
        Setting the resizable parameter to False, configuring the grid of window."""

        self.root = master
        self.root.geometry("1024x768") # set the size of widndow
        self.root.resizable(width=False, height=False) # set the resizble to false
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Initializing frame
        Frame.__init__(self, master)

        # Packing all together and adding widgets
        self.pack()
        self.create_widgets()

    def upload_input(self):
        """Function to upload the input file. """
        # Asking for the input file name.
        self.root.filename = filedialog.askopenfilename(initialdir = "/home/napoleon/course_work/realization",title = "Select file",filetypes = (("input files","*.in"),("all files","*.*")))

        # Trying to read the raw data from file
        self.raw = self.read(self.root.filename)

        # If read successfuly, then insert raw data to text field, clear input name field and insert new file name to it
        if self.raw is not None:
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', self.raw)
            self.text_file_input.delete(0, 'end')
            self.text_file_input.insert(0, self.root.filename)

    def upload_output(self):
        """Function to get the name of output file."""
        self.file_out = filedialog.askopenfilename(initialdir = "/home/napoleon/course_work/realization",title = "Select file",filetypes = (("output files","*.out"),("all files","*.*")))
        self.text_file_output.delete(0, 'end')
        self.text_file_output.insert(0, self.file_out)

    def read(self, input_file):
        """Function to read the contents of input file."""
        try:
            with open(input_file) as file:
                return file.read()
        except (EnvironmentError, TypeError):
            print("Invalid file name. Please try again")
            return None

    def process(self):
        """Function get raw data and passes it to Simulator."""
        self.raw = self.text.get(1.0, 'end')
        self.root.filename = self.text_file_input.get()
        self.file_out = self.text_file_output.get()
        if self.file_out and len(self.raw.split()) != 0 and os.path.isfile(self.file_out) and self.raw:
            self.simulator = Simulator(self.raw, self.file_out, self.root.filename) # self.root.filename - input file
            success = True # flag to check if data is valid
        else:
            messagebox.showerror("Error", "One or both files are missing!")
            success = False

        # show result score
        if success:
            if self.simulator.validate():
                self.score_dialogue()
            else:
                messagebox.showerror("Error", "Invalid input file format!")

    def score_dialogue(self):
        """Function to generate modal score window."""
        dlg = Toplevel() # instantiate modal window
        dlg.wm_title("Result") # set title
        dlg.geometry("210x100") # set resolution
        dlg.resizable(width=False, height=False) # set resizable to false
        text = str(self.simulator.score) # get score text
        l = Label(dlg, text="Your score is :")
        s = Label(dlg, text=text)
        l.grid(row=0, column=0) # set grid
        s.grid(row=1, column=0) # set grid

        # create visualize button
        b = Button(dlg, text="visualize", command=self.visualize, pady=10)
        b.grid(row=2, column=0)
        b["width"] = 15
        b["padx"] = 4

        # a small trick to align the elements of modal window in center
        canvas = Canvas(dlg, width=210, height=100) # there is no use for
        canvas.grid(row=3, column=0)

        dlg.wait_window(dlg) # ask window to be open

    def visualize(self):
        """Function to generate modal window for visualization."""
        vis = Toplevel() # instantiate visualization modal window
        vis.wm_title("Visualization") # set title
        vis.geometry("801x601") # set resolution
        vis.configure(background="#A9A9A9") # set background
        vis.resizable(width=False, height=False) # set resizable
        generator = Button(vis, text="Generate new!", command=self.generate, pady=10) # create generate button
        generator.grid(row=1, column=0) # set grid
        self.canv = Canvas(vis, width=800, height=600, background="#A9A9A9", highlightthickness=0) # create canvas widget for visualization
        self.canv.grid(row=2,column=0)

        vis.grab_set()
        vis.wait_window(vis) # ask window to be open

    def generate(self):
        """Function to emit visualization event."""
        self.canv.delete("all") # clear canvas
        visualizer = Visualizer(self.canv, self.raw, self.file_out) # instantiate Visualizer
        visualizer.visualize() # visualize results

    def show(self):
        self.root.mainloop() # run program
