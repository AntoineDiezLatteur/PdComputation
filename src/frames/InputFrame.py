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

        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Enter Numerical Values")
        self.label.grid(row=0, column=0, columnspan=2, pady=5, padx=10)

        default_values = {"value1": "10.0", "value2": "20.0", "value3": "30.0", "value4": "40.0", "value5": "50.0"}

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        i=1
        for key, value in self.scenario.default_scenario.items():
            if type(value) != str:
                label = ctk.CTkLabel(self, text=f"{key}")
                label.grid(row=i, column=0, pady=5, sticky="w", padx=5)

                entry = ctk.CTkEntry(self)
                entry.grid(row=i, column=1, pady=5, sticky="w", padx=5)

                # entry.insert(0, f"{float(value):.2e}")
                entry.insert(0, 1)
                self.entries[key] = entry
                i+=1

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_values)
        self.submit_button.grid(row=i, column=0, columnspan=2, pady=10, padx=20, sticky="ew")




    def submit_values(self):
        self.values = {key: float(entry.get()) for key, entry in self.entries.items()}
        self.scenario.scenario_generator(scenario=self.values)
        self.scenario.load_scenario('scenario.json')
