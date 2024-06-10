"""
File: LoadFrame
Author: antoi
Date: 07/06/2024
Description: 
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import json


class JsonLoaderFrame(ctk.CTkFrame):
    def __init__(self, master, scenario, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.scenario = scenario
        self.json_path = ""

        # self.pack(fill="both", expand=True)
        self.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="ew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)


        # Button to open file dialog
        self.open_button = ctk.CTkButton(self, text="Browse", command=self.open_file_dialog)
        # self.open_button.pack(pady=20)
        self.open_button.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")

        # Button to load JSON file
        self.load_button = ctk.CTkButton(self, text="Load JSON File", command=self.load_json_file, state="disabled")
        # self.load_button.pack(pady=20)
        self.load_button.grid(row=0, column=3, padx=(5, 10), pady=10, sticky="ew")

        # Text box to display JSON content
        # self.json_textbox = ctk.CTkTextbox(self, width=600, height=400)
        # self.json_textbox.pack(pady=20)

        self.file_entry = ctk.CTkEntry(self, width=400)
        # self.file_entry.pack(pady=20)
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
                # with open(self.json_path, 'r') as file:
                #     data = json.load(file)
                #     formatted_json = json.dumps(data, indent=4)
                #     self.json_textbox.delete("1.0", "end")
                #     self.json_textbox.insert("1.0", formatted_json)
                self.scenario.load_scenario(self.json_path, total_path=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON file: {e}")


# if __name__ == "__main__":
#     app = ctk.CTk()
#     app.geometry("800x600")
#     app.title("JSON Loader")
#
#     frame = JsonLoaderFrame(app)
#     frame.pack(fill="both", expand=True)
#
#     app.mainloop()


