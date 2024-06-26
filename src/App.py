"""
File: Ihm
Author: antoi
Date: 03/06/2024
Description: Manage the different frames and hold the main loop
"""

import customtkinter as ctk
from src import Scenario as scn
from src import Terrain as trn
from src.frames.InputFrame import InputFrame
from src.frames.OutputFrame import OutputFrame
from src.frames.LoadFrame import JsonLoaderFrame

class App(ctk.CTk):
    def __init__(self, config_file='default_config.json'):
        super().__init__()

        self.title("Custom Tkinter HMI")
        self.geometry("800x600")
        self.scenario = scn.Scenario()
        self.terrain = trn.Terrain()
        self.terrain.load_terrain('terrain.json')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.input_frame = InputFrame(master=self, scenario=self.scenario, config_file=config_file)
        self.output_frame = OutputFrame(master=self,scenario=self.scenario, terrain=self.terrain)
        self.load_frame = JsonLoaderFrame(master=self, scenario=self.scenario)
        self.scenario.subscribe(self.input_frame.update)

        print('HMI initialized')

    def main(self):
        self.mainloop()

if __name__ == "__main__":
    app = App(config_file='default_config.json')
    app.main()