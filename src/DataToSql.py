from src.DataToExcel import DataToExcel
import os


class DataToSql:
    directory: str = "files/sql"
    suffix: str = ".sql"

    def __init__(self, data, file: str):
        self.data_string = "\n".join(data)
        self.file = file.removesuffix(DataToExcel.suffix).removeprefix(DataToExcel.prefix)
        self.full_path_file = f"{os.path.abspath(os.getcwd())}/{self.directory}/{self.file}{self.suffix}"
        print("DataToSql:")

    def execute(self):
        with open(self.full_path_file, 'w') as file:
            file.write(self.data_string)

        print(f"{self.full_path_file} SQL-Datei erfolgreich erstellt.")
