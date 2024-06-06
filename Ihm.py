"""
File: Ihm
Author: antoi
Date: 03/06/2024
Description: 
"""

import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import Scenario as scn
from Computation import Computation

class InputFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, scenario, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        self.scenario = scenario

        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Enter Numerical Values")
        self.label.grid(row=0, column=0, columnspan=2, pady=5, padx=10)

        default_values = {"value1": "10.0", "value2": "20.0", "value3": "30.0", "value4": "40.0", "value5": "50.0"}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        i=1
        for key, value in self.scenario.default_scenario.items():
            if type(value) != str:
                label = ctk.CTkLabel(self, text=f"{key}")
                label.grid(row=i, column=0, pady=5, sticky="w", padx=5)

                entry = ctk.CTkEntry(self)
                entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)

                # entry.insert(0, f"{float(value):.2e}")
                entry.insert(0, 1)
                self.entries[key] = entry
                i+=1

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_values)
        self.submit_button.grid(row=i, column=0, columnspan=2, pady=10, padx=20, sticky="ew")




    def submit_values(self):
        self.values = {key: float(entry.get()) for key, entry in self.entries.items()}
        self.scenario.scenario_generator(scenario=self.values)
        self.scenario.load_scenario('scenario.json')

class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, scenario, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
        self.scenario = scenario

        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Output and Graphs")
        self.label.grid(row=0, column=0, pady=5)

        self.run_button = ctk.CTkButton(self, text="Run Program", command=self.run_program)
        self.run_button.grid(row=1, column=0, pady=10)

        self.output_label = ctk.CTkLabel(self, text="")
        self.output_label.grid(row=2, column=0, pady=10)

        self.range_computation_button = ctk.CTkButton(self, text="Display range analysis", command=self.range_computation)
        self.range_computation_button.grid(row=3, column=0, pady=10)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=4, column=0, pady=10, padx=10)

    def run_program(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        Pd = Computation(self.scenario).run()
        # self.output_label.configure(text=f"Computed Result: {np.max(y)}")
        self.output_label.configure(text=f"Computed Pd: {Pd}")

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        self.canvas.draw()

    def range_computation(self):
        print('Range computation')
        pass

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