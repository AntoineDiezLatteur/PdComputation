"""
File: InputFrame
Author: antoi
Date: 06/06/2024
Description: Hold the input frame for the HMI
"""

import customtkinter as ctk

class InputFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, scenario, config_file, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        self.__scenario = scenario
        self.entries = {}
        self._config_file = config_file
        self.create_widgets()

    @property
    def scenario(self):
        return self.__scenario

    @scenario.setter
    def scenario(self, value):
        self.__scenario = value

    def create_widgets(self):
        self.config_button = ctk.CTkButton(self, text="Load Configuration", command=self.configure_scenario)
        self.config_button.grid(row=0, column=0, pady=10, padx=20, columnspan=2, sticky="ew")

        self.label = ctk.CTkLabel(self, text="Enter Numerical Values")
        self.label.grid(row=1, column=0, columnspan=2, pady=(10, 5), padx=(10, 5), sticky="ew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        i=2
        for key in self.scenario.scenario_parameters:

            label = ctk.CTkLabel(self, text=f"{key}")
            label.grid(row=i, column=0, pady=5, sticky="w", padx=5)

            entry = ctk.CTkEntry(self, placeholder_text='Enter a value')
            entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)
            self.entries[key] = entry
            i+=1

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_values)
        self.submit_button.grid(row=i, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

    def configure_scenario(self):
        self.scenario.config(self._config_file)
        print("Scenario configured")

    def update(self, new_scenario):
        for key, value in self.scenario.scenario_parameters.items():
            if key in self.entries:
                if key == 'swelring_model' or key == 'Nb' or key == 'Kb':
                    self.entries[key].delete(0, 'end')
                    self.entries[key].insert(0, int(value))
                else:
                    self.entries[key].delete(0, 'end')
                    self.entries[key].insert(0, float(value))


    def submit_values(self):
        scenario = {key: float(entry.get()) for key, entry in self.entries.items()}
        self.scenario.scenario_parameters = scenario
        print("Values submitted")

