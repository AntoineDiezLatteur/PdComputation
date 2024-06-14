"""
File: OutputFrame
Author: antoi
Date: 06/06/2024
Description: Hold the output frame and display the results
"""

import customtkinter as ctk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.Computation import Computation

class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, scenario, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=1, padx=(5, 10), pady=(10, 10), sticky="nswe")
        self.__scenario = scenario

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.create_widgets()

    @property
    def scenario(self):
        return self.__scenario

    @scenario.setter
    def scenario(self, value):
        self.__scenario = value

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Output and Graphs")
        self.label.grid(row=0, column=0, pady=5)

        self.range_computation_button = ctk.CTkButton(self, text="Run computation", command=self.run_program)
        self.range_computation_button.grid(row=1, column=0, pady=10)

        self.selected_option = ctk.StringVar(value="Pd computation")

        self.option_menu = ctk.CTkOptionMenu(
            self,
            variable=self.selected_option,
            values=["Pd computation", "Snr computation"],
            command=self.on_option_selected
        )
        self.option_menu.grid(row=2, column=0, pady=10)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=4, column=0, pady=(10, 20), padx=20, sticky="nswe")

    def on_option_selected(self, value):
        pass

    def run_program(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if self.selected_option.get() == "Pd computation":
            x, y, z, w = Computation(self.scenario).pd_analysis()
            thr = [self.scenario.config_parameters['desired_pd'] for _ in range(len(x))]
            ax.plot(x, y)
            ax.plot(x, z)
            ax.plot(x, w)
            ax.plot(x, thr, c='r', linestyle='--')
            ax.legend(['Pd w/ clutter', 'Pd w/o clutter', 'Pd w/ clutter in sidelobe', 'Desired Pd'])

        elif self.selected_option.get() == "Snr computation":
            x, y, z, w = Computation(self.scenario).snr_analysis()
            ax.plot(x, y)
            ax.plot(x, z)
            ax.plot(x, w)
            ax.legend(['Snr w/ clutter', 'Snr w/o clutter', 'Snr w/ clutter in sidelobe', 'Desired Pd'])
        self.canvas.draw()
        print("Computation done")