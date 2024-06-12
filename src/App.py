"""
File: Ihm
Author: antoi
Date: 03/06/2024
Description: 
"""

import customtkinter as ctk
from src import Scenario as scn
from src.frames.InputFrame import InputFrame
from src.frames.OutputFrame import OutputFrame
from src.frames.LoadFrame import JsonLoaderFrame

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
        self.load_frame = JsonLoaderFrame(master=self, scenario=self.scenario)

        print('HMI initialized')
        # self.mainloop()

    def main(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.main()