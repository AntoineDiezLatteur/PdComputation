"""
File: Ihm
Author: antoi
Date: 03/06/2024
Description: 
"""
#
# import tkinter as tk
# import Scenario as scn
# import Computation as cpt
#
# class Ihm(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Radar Simulation")
#         self.geometry("800x600")
#         self.create_widgets()
#         self.scenario = scn.Scenario()
#         self.scenario.load_scenario('scenario.json')
#
#     def create_widgets(self):
#         self.label = tk.Label(self, text="Radar Simulation")
#         self.label.pack()
#
#         self.button = tk.Button(self, text="Run simulation", command=self.on_button_click)
#         self.button.pack()
#
#         self.entry = tk.Entry(self)
#         self.entry.pack()
#
#         self.var = tk.IntVar(self)
#         self.radiobutton1 = tk.Radiobutton(self, text="Option 1", variable=self.var, value=1)
#         self.radiobutton2 = tk.Radiobutton(self, text="Option 2", variable=self.var, value=2)
#         self.radiobutton1.pack()
#         self.radiobutton2.pack()
#
#         self.listbox = tk.Listbox(self)
#         self.listbox.pack()
#         self.listbox.insert(tk.END, "Item 1")
#         self.listbox.insert(tk.END, "Item 2")
#
#         # self.button = tk.Button(self, text="Run simulation", command=self.run_simulation)
#         # self.button.pack()
#         #
#         # self.quit_button = tk.Button(self, text="Quit", command=self.quit)
#         # self.quit_button.pack()
#
#     def on_button_click(self):
#         print("Button clicked")
#         # self.scenario.load_scenario('scenario.json')
#         self.computation = cpt.Computation(self.scenario)
#         self.computation.run()
#
#
#
#     def run(self):
#         self.mainloop()
#         print("Simulation running")
#         print(self.entry)
#
#
# if __name__ == '__main__':
#     Ihm().run()

import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class InputFrame(ctk.CTkFrame):
    def __init__(self, master, scenario, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        self.scenario = scenario
        self.scenario.load_scenario('scenario.json')

        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Enter Numerical Values")
        self.label.grid(row=0, column=0, columnspan=2, pady=5, padx=10)

        default_values = {"value1": "10.0", "value2": "20.0", "value3": "30.0", "value4": "40.0", "value5": "50.0"}

        # for i in range(1, 6):
        #     label = ctk.CTkLabel(self, text=f"Value {i}")
        #     label.grid(row=i, column=0, pady=5, sticky="e", padx=5)
        #
        #     entry = ctk.CTkEntry(self)
        #     entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)
        #     entry.insert(0, default_values[f"value{i}"])
        #     self.entries[f"value{i}"] = entry
        #
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        # self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_values)
        # self.submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

        for key in self.scenario.default_scenario.keys():
            label = ctk.CTkLabel(self, text=f"{key}")
            label.grid(row=i, column=0, pady=5, sticky="e", padx=5)

            entry = ctk.CTkEntry(self)
            entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)
            entry.insert(0, self.scenario.default_scenario[key])
            self.entries[key] = entry


    def submit_values(self):
        self.values = {key: float(entry.get()) for key, entry in self.entries.items()}
        print(self.values)  # For debugging

class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, scenario, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
        self.scenario = scenario

        # Configure grid to center widgets
        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_rowconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Output and Graphs")
        self.label.grid(row=0, column=0, pady=5)

        self.run_button = ctk.CTkButton(self, text="Run Program", command=self.run_program)
        self.run_button.grid(row=1, column=0, pady=10)

        self.output_label = ctk.CTkLabel(self, text="")
        self.output_label.grid(row=2, column=0, pady=10)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=3, column=0, pady=10, padx=10)

    def run_program(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        Computation(self.scenario).run()
        self.output_label.configure(text=f"Computed Result: {np.max(y)}")

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        self.canvas.draw()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Custom Tkinter HMI")
        self.geometry("800x600")
        self.scenario = scn.Scenario()
        self.scenario.load_scenario('scenario.json')

        # Configure the grid layout for the main window
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.input_frame = InputFrame(master=self, scenario=self.scenario)
        self.output_frame = OutputFrame(master=self,scenario=self.scenario)

if __name__ == "__main__":
    app = App()
    app.mainloop()