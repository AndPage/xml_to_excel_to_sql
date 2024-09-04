from src.FileSelectorApp import FileSelectorApp
from src.XMLReader import XMLReader
from src.SequenceCreator import SequenceCreator
from src.DataCreator import DataCreator
from src.DataToExcel import DataToExcel
from src.ExcelReader import ExcelReader
from src.SqlCreator import SqlCreator
from src.DataToSql import DataToSql
import os


def xml_workflow():
    reader = XMLReader(os.path.abspath(f"{selected_directory}/{selected_file}"))
    reader.load_xml()
    parsed_xml = reader.getParsedXML()
    # print(parsed_xml)

    sequenceCreator = SequenceCreator(parsed_xml)
    sequenceTableIds = sequenceCreator.getSequence()
    print(sequenceTableIds)

    dataCreator = DataCreator(sequenceTableIds, parsed_xml)
    data_table = dataCreator.get_table()

    dataToExcel = DataToExcel(data_table, selected_file)
    dataToExcel.execute()


def excel_workflow():
    excelReader = ExcelReader(os.path.abspath(f"{selected_directory}/{selected_file}"))
    data_dict = excelReader.get_parsed_excel()
    # print(data_dict)

    sqlCreator = SqlCreator(data_dict)
    sql_list = sqlCreator.get_sql_data()

    dataToSql = DataToSql(sql_list, selected_file)
    dataToSql.execute()


if __name__ == "__main__":
    fileSelectorApp = FileSelectorApp()
    selected_file = fileSelectorApp.get_selected_file_name()
    selected_directory = fileSelectorApp.get_selected_directory()
    print(f"Selected file: {os.path.abspath(f"{selected_directory}/{selected_file}")}")

    if selected_directory == fileSelectorApp.directories['XML']:
        xml_workflow()
    elif selected_directory == fileSelectorApp.directories['Excel']:
        excel_workflow()
