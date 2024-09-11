import os

from src.DataToSql import DataToSql
from src.ExcelReader import ExcelReader
from src.InsertCreator import InsertCreator
from src.SqlToDb import SqlToDb

if __name__ == "__main__":
    folder = "files"
    file = "wertebereiche.xlsx"
    excelReader = ExcelReader(os.path.abspath(f"{folder}/{file}"))
    data_dict = excelReader.get_parsed_insert_into()

    insertCreator = InsertCreator(data_dict)
    sql_list = insertCreator.get_sql_data()

    for k, v in sql_list.items():
        dataToSql = DataToSql(v, k)
        dataToSql.execute()

        sqlToData = SqlToDb(dataToSql.full_path_file)
