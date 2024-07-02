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
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation
import math

class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, scenario, terrain, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=1, padx=(5, 10), pady=(10, 10), sticky="nswe")
        self.__scenario = scenario
        self.__terrain = terrain
        self.__results = {}

        self.ani1 = None
        self.ani2 = None

        self.frame_idx = 0  # Shared frame index
        self.direction = 1  # Shared direction

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

    @property
    def results(self):
        return self.__results

    @results.setter
    def results(self, value):
        self.__results = value

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Output and Graphs")
        self.label.grid(row=0, column=0, pady=5)

        self.range_computation_button = ctk.CTkButton(self, text="Run computation", command=self.run_program)
        self.range_computation_button.grid(row=1, column=0, pady=10)

        self.display_button = ctk.CTkButton(self, text="Display results", command=self.open_new_window)
        self.display_button.grid(row=3, column=0, pady=10)

        self.selected_option = ctk.StringVar(value="Single scan Pd")

        self.option_menu = ctk.CTkOptionMenu(
            self,
            variable=self.selected_option,
            values=["Single scan Pd", "Multi-scan Pd", "Snr", "Visibility", "Terrain"],
            command=self.on_option_selected
        )
        self.option_menu.grid(row=2, column=0, pady=10)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=4, column=0, pady=(10, 20), padx=20, sticky="nswe")

    def on_option_selected(self, value):
        pass

    def open_new_window(self):
        new_window = ctk.CTkToplevel(self.master)
        new_window.geometry("800x600")
        new_window.title(f'{self.selected_option.get()} results')

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=new_window)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True, pady=(10, 5), padx=10)

        button = ctk.CTkButton(new_window, text="Close", command=new_window.destroy)
        button.pack(side=ctk.BOTTOM, pady=(5, 10))

        button_animate = ctk.CTkButton(new_window, text="Start Animation", command=self.start_animation)
        button_animate.pack(side=ctk.BOTTOM, pady=(5, 10))

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if self.selected_option.get() == "Single scan Pd":
            x = self.results['range']
            y1 = self.results['single_scan']['Pd_w_clutter']
            y2 = self.results['single_scan']['Pd_w_o_clutter']
            y3 = self.results['single_scan']['Pd_w_clutter_in_sidelobe']
            thr = [self.scenario.config_parameters['desired_pd'] for _ in range(len(x))]
            ax.plot(x, y1)
            ax.plot(x, y2)
            ax.plot(x, y3)
            ax.plot(x, thr, c='r', linestyle='--')
            ax.legend(['Pd w/ clutter', 'Pd w/o clutter', 'Pd w/ clutter in sidelobe'])
            ax.title.set_text('Single scan Pd')

        elif self.selected_option.get() == "Multi-scan Pd":
            x = self.results['range']
            z1 = self.results['multi_scan']['Pd_w_clutter']
            z2 = self.results['multi_scan']['Pd_w_o_clutter']
            z3 = self.results['multi_scan']['Pd_w_clutter_in_sidelobe']
            thr = [self.scenario.config_parameters['desired_pd'] for _ in range(len(x))]
            ax.plot(x, z1)
            ax.plot(x, z2)
            ax.plot(x, z3)
            ax.plot(x, thr, c='r', linestyle='--')
            ax.legend(['Pd w/ clutter', 'Pd w/o clutter', 'Pd w/ clutter in sidelobe'])
            ax.title.set_text('Multi-scan Pd')

        elif self.selected_option.get() == "Snr":
            x = self.results['range']
            w1 = self.results['snr']['Snr_w_clutter']
            w2 = self.results['snr']['Snr_w_o_clutter']
            w3 = self.results['snr']['Snr_w_clutter_in_sidelobe']
            ax.plot(x, w1)
            ax.plot(x, w2)
            ax.plot(x, w3)
            ax.legend(['Snr w/ clutter', 'Snr w/o clutter', 'Snr w/ clutter in sidelobe'])
            ax.title.set_text('Snr')

        elif self.selected_option.get() == "Visibility":
            x = self.results['range']
            j1 = self.results['visibility']['target']
            j2 = self.results['visibility']['clutter']
            j3 = self.results['visibility']['clutter_idx']
            j4 = self.results['visibility']['target_idx']

            # Create segments
            points = np.array([x, j1]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            colors_list = ['red', 'green', 'blue']  # Define a list of colors to use
            colors = []
            # Dynamically assign colors based on the length of color_change_indices
            for i in range(len(j4)):
                if i == 0:
                    colors.extend([colors_list[i]] * j4[i])
                else:
                    colors.extend([colors_list[i]] * (j4[i] - j4[i - 1]))

            # Create a LineCollection from the segments
            lc = LineCollection(segments, colors=colors, linewidth=2)

            # Create a plot
            ax.add_collection(lc)

        elif self.selected_option.get() == "Terrain":
            x = self.results['range']
            k1 = self.results['terrain']['idx']
            k2 = self.results['terrain']['height']
            ax.plot(x, k1)
            ax.plot(x, k2)
            ax.legend(['Terrain index', 'Terrain height', 'Terrain visibility'])
            ax.title.set_text('Terrain')

        self.canvas.draw()

    def start_animation(self):
        ax = self.figure.gca()
        x = self.results['range']
        y1 = self.results['single_scan']['Pd_w_clutter']
        y2 = self.results['single_scan']['Pd_w_clutter_in_sidelobe']

        targetpd1, = ax.plot([], [], 'ro', markersize=5)
        targetpd2, = ax.plot([], [], 'ro', markersize=5)

        def initpd():
            targetpd1.set_data([], [])
            targetpd2.set_data([], [])
            return [targetpd1, targetpd2]

        def updatepd(frame):
            self.frame_idx += self.direction
            if self.frame_idx >= len(x) - 1 or self.frame_idx <= 0:
                self.direction *= -1
            targetpd1.set_data(x[self.frame_idx], y1[self.frame_idx])
            targetpd2.set_data(x[self.frame_idx], y2[self.frame_idx])
            return [targetpd1, targetpd2]

        if self.ani1:
            self.ani1.event_source.stop()

        self.ani1 = FuncAnimation(self.figure, updatepd, frames=len(x), init_func=initpd, blit=True, repeat=True, interval=10)
        self.canvas.draw()

    def run_program(self):
        # Clear the figure and axes
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        x = self.terrain.range
        y = self.terrain.height
        z = [self.scenario.scenario_parameters['target_height'] for _ in range(len(x))]

        ax.plot(x, y, c='g')
        ax.plot(x, z, c='b', linestyle='--')
        ax.scatter(0, self.scenario.scenario_parameters['radar_height'], c='black', marker='o')
        ax.legend(['Terrain height', 'Target trajectory', 'Radar position'])
        ax.title.set_text('Scenario and terrain configuration')

        beam_length = max(x)  # You can adjust the length of the beam as needed
        angle_rad = np.deg2rad(1.5)  # Convert 1.5 degrees to radians
        tilt_angle_rad = np.deg2rad(5)  # Convert tilt angle to radians
        radar_height = self.scenario.scenario_parameters['radar_height']

        ax.set_ylim(0, max(z) + 100)
        ax.set_xscale('linear')

        self.canvas.draw()

        target, = ax.plot([], [], 'ro', markersize=5)
        beam_center, = ax.plot([], [], 'r--', lw=1)

        def init():
            target.set_data([], [])
            beam_center.set_data([], [])
            return target, beam_center

        def update(frame):
            self.frame_idx += self.direction
            if self.frame_idx >= len(x) - 1 or self.frame_idx <= 0:
                self.direction *= -1
            target.set_data(x[self.frame_idx], z[self.frame_idx])
            x_coord = x[self.frame_idx]
            y_coord = z[self.frame_idx]
            h = self.scenario.scenario_parameters['radar_height']
            theta = math.atan2(y_coord - h, x_coord)

            beam_center_x = beam_length * np.cos(theta)
            beam_center_y = h + beam_length * np.sin(theta)
            beam_center.set_data([0, beam_center_x], [h, beam_center_y])

            return target, beam_center

        if self.ani2:
            self.ani2.event_source.stop()

        self.ani2 = FuncAnimation(self.figure, update, frames=len(x), init_func=init, blit=True, repeat=True, interval=10)

        x, y1, y2, y3, z1, z2, z3, w1, w2, w3, j1, j2, j3, j4, k1, k2 = Computation(self.scenario, self.terrain).computation_loop()

        self.results = {
            'range': x,
            'single_scan': {
                'Pd_w_clutter': y1,
                'Pd_w_o_clutter': y2,
                'Pd_w_clutter_in_sidelobe': y3,
            },
            'multi_scan': {
                'Pd_w_clutter': z1,
                'Pd_w_o_clutter': z2,
                'Pd_w_clutter_in_sidelobe': z3,
            },
            'snr': {
                'Snr_w_clutter': w1,
                'Snr_w_o_clutter': w2,
                'Snr_w_clutter_in_sidelobe': w3,
            },
            'visibility': {
                'target_idx': j1,
                'clutter_idx': j2,
                'clutter': j3,
                'target': j4,
            },
            'terrain': {
                'idx': k1,
                'height': k2,
            }
        }

        print("computation done")