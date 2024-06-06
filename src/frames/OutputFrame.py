"""
File: OutputFrame
Author: antoi
Date: 06/06/2024
Description: 
"""

import customtkinter as ctk
import numpy as np
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