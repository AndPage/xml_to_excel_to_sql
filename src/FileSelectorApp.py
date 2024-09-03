import os
import tkinter as tk
from tkinter import ttk


class FileSelectorApp(tk.Tk):
    directory: str = "xml_files"
    selected_file_name: str = ''

    def __init__(self):
        super().__init__()
        self.title("Dateiauswahl")

        self.frame = ttk.Frame(self, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.label = ttk.Label(self.frame, text=f"Chose your File from '{self.directory}'")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.combo = ttk.Combobox(self.frame)
        self.combo.grid(row=1, column=0, padx=5, pady=5)
        self.combo.bind("<<ComboboxSelected>>", self.on_select)
        self.combo["values"] = self.list_files(self.directory)

        self.mainloop()

    def list_files(self, directory):
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    def on_select(self, event):
        self.selected_file_name = self.combo.get()
        self.destroy()

    def get_selected_file_name(self):
        return self.selected_file_name
