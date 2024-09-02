from src.FileSelectorApp import FileSelectorApp
from src.XMLReader import XMLReader
from src.SequenceCreator import SequenceCreator
from src.DataCreator import DataCreator
import os

if __name__ == "__main__":
    fileSelectorApp = FileSelectorApp()
    selected_file = fileSelectorApp.get_selected_file_name()
    print(f"Selected file: {os.path.abspath(selected_file)}")

    reader = XMLReader(os.path.abspath(selected_file))
    reader.load_xml()
    parsed_xml = reader.getParsedXML()
    # print(parsed_xml)

    sequenceCreator = SequenceCreator(parsed_xml)
    sequenceTableIds = sequenceCreator.getSequence()
    print(sequenceTableIds)

    dataCreator = DataCreator(sequenceTableIds, parsed_xml)
    data_table = dataCreator.get_table()

    print(*range(len(sequenceTableIds)))
