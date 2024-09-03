from src.DataToExcel import DataToExcel
import os


class DataToSql:
    directory: str = "sql_output"
    suffix: str = ".sql"

    def __init__(self, data, file: str):
        self.data_string = "\n".join(data)
        self.path = os.path.abspath(os.getcwd())
        self.file = file.removesuffix(DataToExcel.suffix).removeprefix(DataToExcel.prefix)

    def execute(self):
        with open(f"{self.path}/{self.directory}/{self.file}{self.suffix}", 'w') as file:
            file.write(self.data_string)
