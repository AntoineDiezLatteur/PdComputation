"""
File: InputFrame
Author: antoi
Date: 06/06/2024
Description: 
"""
import customtkinter as ctk

class InputFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, scenario, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        self.scenario = scenario

        self.variables = {}
        self.create_widgets()

    def create_widgets(self):
        self.config_button = ctk.CTkButton(self, text="Configure Scenario", command=self.configure_scenario)
        self.config_button.grid(row=0, column=0, pady=10, padx=20, columnspan=2, sticky="ew")

        self.label = ctk.CTkLabel(self, text="Enter Numerical Values")
        self.label.grid(row=1, column=0, columnspan=2, pady=(10, 5), padx=(10, 5), sticky="ew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        i=2
        for name in self.scenario.scenario_parameter_list:

            label = ctk.CTkLabel(self, text=f"{name}")
            label.grid(row=i, column=0, pady=5, sticky="w", padx=5)

            entry = ctk.CTkEntry(self, placeholder_text='Enter a value')
            entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)
            self.variables[name] = entry

            i+=1

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_values)
        self.submit_button.grid(row=i, column=0, columnspan=2, pady=10, padx=20, sticky="ew")


    def configure_scenario(self):
        print(self.scenario)
        self.scenario.config()
        print(self.scenario)

    def update(self, new_scenario):
        print('Updating input frame')
        for key, value in self.scenario.scenario.items():
            if key in self.variables:
                self.variables[key].delete(0, 'end')
                self.variables[key].insert(0, value)


    def submit_values(self):
        scenario = {key: float(entry.get()) for key, entry in self.variables.items()}
        self.scenario.scenario = scenario

