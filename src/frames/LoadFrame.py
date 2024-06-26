"""
File: LoadFrame
Author: antoi
Date: 07/06/2024
Description: Hold the load frame for the HMI. Load a JSON file and update the scenario
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
from src.loader import DATA_PATH

class JsonLoaderFrame(ctk.CTkFrame):
    def __init__(self, master, scenario, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.__scenario = scenario
        self.json_path = DATA_PATH + '/default_scenario.json'

        self.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="ew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        self.create_widgets()

    @property
    def scenario(self):
        return self.__scenario

    @scenario.setter
    def scenario(self, value):
        self.__scenario = value

    def create_widgets(self):

        self.open_button = ctk.CTkButton(self, text="Browse", command=self.open_file_dialog)
        self.open_button.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")

        if self.json_path:
            self.load_button = ctk.CTkButton(self, text="Load JSON scenario", command=self.load_json_file, state="normal")
        else:
            self.load_button = ctk.CTkButton(self, text="Load JSON scenario", command=self.load_json_file, state="disabled")

        self.load_button.grid(row=0, column=3, padx=(5, 10), pady=10, sticky="ew")

        self.file_entry = ctk.CTkEntry(self, width=400)
        self.file_entry.delete(0, "end")
        self.file_entry.insert(0, self.json_path)
        self.file_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=10, sticky="ew")

    def open_file_dialog(self):
        self.json_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if self.json_path:
            self.load_button.configure(state="normal")
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, self.json_path)
        else:
            self.load_button.configure(state="disabled")

    def load_json_file(self):
        if self.json_path:
            try:
                self.scenario.load_scenario(self.json_path, total_path=True)
                print("Scenario loaded")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON file: {e}")