"""
File: OutputFrame
Author: antoi
Date: 06/06/2024
Description: Hold the output frame and display the results
"""

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.computation.Computation import Computation

class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, scenario, terrain, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=1, padx=(5, 10), pady=(10, 10), sticky="nswe")
        self.__scenario = scenario
        self.__terrain = terrain

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.create_widgets()

    @property
    def scenario(self):
        return self.__scenario

    @scenario.setter
    def scenario(self, value):
        self.__scenario = value

    @property
    def terrain(self):
        return self.__terrain

    @terrain.setter
    def terrain(self, value):
        self.__terrain = value

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Output and Graphs")
        self.label.grid(row=0, column=0, pady=5)

        self.range_computation_button = ctk.CTkButton(self, text="Run computation", command=self.run_program)
        self.range_computation_button.grid(row=1, column=0, pady=10)

        self.selected_option = ctk.StringVar(value="Single scan Pd")

        self.option_menu = ctk.CTkOptionMenu(
            self,
            variable=self.selected_option,
            values=["Single scan Pd", "Multi-scan Pd", "Snr computation"],
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
        ax1, ax2 = self.figure.subplots(2,1)

        ax1.set_position([0.1, 0.35, 0.8, 0.6])  # [left, bottom, width, height]
        ax2.set_position([0.1, 0.1, 0.8, 0.2])  # [left, bottom, width, height]

        x2 = self.terrain.range
        y2 = self.terrain.height
        z2 = [self.scenario.scenario_parameters['target_height'] for _ in range(len(x2))]

        if self.selected_option.get() == "Single scan Pd":
            print('single scan')
            x, y, z, w, j, k, l = Computation(self.scenario, self.terrain).computation_loop()
            thr = [self.scenario.config_parameters['desired_pd'] for _ in range(len(x))]
            ax1.plot(x, y)
            ax1.plot(x, z)
            ax1.plot(x, w)
            ax1.plot(x, thr, c='r', linestyle='--')
            ax1.legend(['Pd w/ clutter', 'Pd w/o clutter', 'Pd w/ clutter in sidelobe', 'Desired Pd'])

        elif self.selected_option.get() == "Multi-scan Pd":
            x, y, z, w, j, k, l = Computation(self.scenario).computation_loop(mutli_scan_mode=True)
            thr = [self.scenario.config_parameters['desired_pd'] for _ in range(len(x))]
            ax1.plot(x, y)
            ax1.plot(x, z)
            ax1.plot(x, w)
            ax1.plot(x, thr, c='r', linestyle='--')
            ax1.legend(['Pd w/ clutter', 'Pd w/o clutter', 'Pd w/ clutter in sidelobe', 'Desired Pd'])

        elif self.selected_option.get() == "Snr computation":
            x, y, z, w, j, k, l = Computation(self.scenario).computation_loop(snr_mode=True)
            ax1.plot(x, y)
            ax1.plot(x, z)
            ax1.plot(x, w)
            ax1.legend(['Snr w/ clutter', 'Snr w/o clutter', 'Snr w/ clutter in sidelobe', 'Desired Pd'])
        ax2.plot(x2, y2, c='g')
        ax2.plot(x2, z2, c='b', linestyle='--')
        ax2.scatter(0, self.scenario.scenario_parameters['radar_height'], c='black', marker='o')

        self.canvas.draw()
        print("computation done")