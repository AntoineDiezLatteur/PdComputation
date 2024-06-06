"""
File: Ihm
Author: antoi
Date: 03/06/2024
Description: 
"""

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from src import Scenario as scn
from src.Computation import Computation
from src.frames.InputFrame import InputFrame
from src.frames.OutputFrame import OutputFrame





class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Custom Tkinter HMI")
        self.geometry("800x600")
        self.scenario = scn.Scenario()
        self.scenario.scenario_generator()

        # Configure the grid layout for the main window
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.input_frame = InputFrame(master=self, scenario=self.scenario)
        self.output_frame = OutputFrame(master=self,scenario=self.scenario)
        print('HMI initialized')

if __name__ == "__main__":
    app = App()
    app.mainloop()