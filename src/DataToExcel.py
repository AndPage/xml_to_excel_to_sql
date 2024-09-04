import pandas as pd
import os


class DataToExcel:
    directory: str = "excel_output"
    prefix: str = "datadictionary_"
    suffix: str = ".xlsx"

    def __init__(self, datasheet, file: str):
        self.path = os.path.abspath(os.getcwd())
        self.datasheet = datasheet
        self.file = file.removesuffix('.xml')
        print(self.file)

    def execute(self):
        tables = {}
        for entry in self.datasheet:
            table_name = entry.pop('table')
            if table_name not in tables:
                tables[table_name] = []
            tables[table_name].append(entry)

        # DataFrames in Excel speichern
        with pd.ExcelWriter(f"{self.path}/{self.directory}/{self.prefix}{self.file}{self.suffix}") as writer:
            for table_name, rows in tables.items():
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=table_name, index=False)

        print(f"/{self.directory}/{self.prefix}{self.file}{self.suffix} Excel-Datei erfolgreich erstellt.")
