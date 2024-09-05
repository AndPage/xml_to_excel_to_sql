import pandas as pd
import os


class DataToExcel:
    directory: str = "files/excel"
    prefix: str = "datadictionary_"
    suffix: str = ".xlsx"

    def __init__(self, datasheet, file: str):
        self.path = os.path.abspath(os.getcwd())
        self.datasheet = datasheet
        self.file = file.removesuffix('.xml')
        print(self.file)

    def execute(self):
        pd.DataFrame(self.datasheet).to_excel(f"{self.path}/{self.directory}/{self.prefix}{self.file}{self.suffix}", index=False)

        print(f"/{self.directory}/{self.prefix}{self.file}{self.suffix} Excel-Datei erfolgreich erstellt.")
