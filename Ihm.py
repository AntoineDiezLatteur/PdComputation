"""
File: Ihm
Author: antoi
Date: 03/06/2024
Description: 
"""

import tkinter as tk
import Scenario as scn
import Computation as cpt

class Ihm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Radar Simulation")
        self.geometry("800x600")
        self.create_widgets()
        # self.scenario = scn.Scenario()

    def create_widgets(self):
        self.label = tk.Label(self, text="Radar Simulation")
        self.label.pack()

        # self.button = tk.Button(self, text="Run simulation", command=self.run_simulation)
        # self.button.pack()
        #
        # self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        # self.quit_button.pack()



    def run(self):
        self.mainloop()
        print("Simulation running")


if __name__ == '__main__':
    Ihm().run()