import pandas as pd


class ExcelReader:
    parsed_excel: list = []
    raw_data = None

    def __init__(self, file_path):
        self.read_excel_file(file_path)

    def read_excel_file(self, file_path):
        self.raw_data = pd.read_excel(file_path, sheet_name=None)

    def parse_excel(self):
        for sheet_name, df in self.raw_data.items():
            df = df.fillna('')  # Leere Zellen als leere Strings behandeln
            for index, row in df.iterrows():
                row_dict = {"table": sheet_name}
                for col_name in df.columns:
                    row_dict[col_name] = row[col_name]
                self.parsed_excel.append(row_dict)

    def get_parsed_excel(self):
        self.parse_excel()
        return self.parsed_excel


if __name__ == "__main__":
    excelReader = ExcelReader("/home/dev/projects/draw_io_to_sql/excel_input/datadictionary_test.drawio.xlsx")
    data_dict = excelReader.get_parsed_excel()

    for entry in data_dict:
        print(entry)
