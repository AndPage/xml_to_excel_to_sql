import pandas as pd


class ExcelReader:
    parsed_excel_list: list = []
    parsed_excel_dict: dict = {}
    raw_data = None

    def __init__(self, file_path):
        self.read_excel_file(file_path)

    def read_excel_file(self, file_path):
        self.raw_data = pd.read_excel(file_path, sheet_name=None)

    def parse_data_dict(self):
        for sheet_name, df in self.raw_data.items():
            df = df.fillna('')  # Leere Zellen als leere Strings behandeln
            for index, row in df.iterrows():
                row_dict = {}
                for col_name in df.columns:
                    row_dict[col_name] = row[col_name]
                self.parsed_excel_list.append(row_dict)

    def parse_insert_into(self):
        for sheet_name, df in self.raw_data.items():
            df = df.fillna('')  # Leere Zellen als leere Strings behandeln
            row_list = []
            for index, row in df.iterrows():
                row_dict = {}
                for col_name in df.columns:
                    row_dict[col_name] = self.add_leading_zeros(str(row[col_name]))
                row_list.append(row_dict)

            self.parsed_excel_dict[sheet_name] = row_list

    @staticmethod
    def add_leading_zeros(field: str) -> str:
        if field.isdigit() and len(field) == 4:
            return field.zfill(5)
        return field

    def get_parsed_data_dict(self):
        self.parse_data_dict()
        return self.parsed_excel_list

    def get_parsed_insert_into(self):
        self.parse_insert_into()

        # for key, entry in self.parsed_excel_dict.items():
        #     print(key)
        #     i = 0
        #     for item in entry:
        #         print(f"    {item}")
        #         i += 1
        #         if i == 10:
        #             break

        return self.parsed_excel_dict


if __name__ == "__main__":
    # excelReader = ExcelReader("/home/dev/projects/draw_io_to_sql/files/excel/datadictionary_project.drawio.xlsx")
    # data_dict = excelReader.get_parsed_data_dict()
    #
    # for entry in data_dict:
    #     print(entry)

    excelReader = ExcelReader("/home/dev/projects/draw_io_to_sql/files/excel/wertebereiche.xlsx")
    data_dict = excelReader.get_parsed_insert_into()
