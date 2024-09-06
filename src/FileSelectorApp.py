import os
import tkinter as tk
from tkinter import ttk


class FileSelectorApp(tk.Tk):
    directories = {"XML": "files/xml", "Excel": "files/excel"}
    selected_file_name: str = ''
    selected_directory: str = ''

    def __init__(self):
        super().__init__()
        self.title("Dateiauswahl")

        self.frame = ttk.Frame(self, padding="10")
        self.frame.grid(row=0, column=0, sticky="n, e, s, w")

        self.dir_label = ttk.Label(self.frame, text="Wähle das Ausgangsformat:")
        self.dir_label.grid(row=0, column=0, padx=5, pady=5)

        self.dir_combo = ttk.Combobox(self.frame, values=list(self.directories.keys()))
        self.dir_combo.grid(row=1, column=0, padx=5, pady=5)
        self.dir_combo.bind("<<ComboboxSelected>>", self.on_directory_select)

        self.file_label = ttk.Label(self.frame, text="Wähle die Datei:")
        self.file_label.grid(row=2, column=0, padx=5, pady=5)

        self.file_combo = ttk.Combobox(self.frame)
        self.file_combo.grid(row=3, column=0, padx=5, pady=5)
        self.file_combo.bind("<<ComboboxSelected>>", self.on_file_select)

        self.mainloop()

    @staticmethod
    def list_files(directory):
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    def on_directory_select(self, event):
        selected_dir_key = self.dir_combo.get()
        self.selected_directory = self.directories[selected_dir_key]
        self.file_combo["values"] = self.list_files(self.selected_directory)

    def on_file_select(self, event):
        self.selected_file_name = self.file_combo.get()
        self.destroy()

    def get_selected_file_name(self):
        return self.selected_file_name

    def get_selected_directory(self):
        return self.selected_directory


if __name__ == "__main__":
    app = FileSelectorApp()
    print(f"Ausgewählter Ordner: {app.get_selected_directory()}")
    print(f"Ausgewählte Datei: {app.get_selected_file_name()}")
