"""
File: Ihm
Author: antoi
Date: 03/06/2024
Description: 
"""

import tkinter as tk

class Ihm(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Radar Simulation")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Radar Simulation")
        self.label.pack()

        self.button = tk.Button(self, text="Run simulation", command=self.run_simulation)
        self.button.pack()

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.pack()

    def run_simulation(self):
        print("Simulation running")