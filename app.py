from src.FileSelectorApp import FileSelectorApp
from src.XMLReader import XMLReader
import os

if __name__ == "__main__":
    fileSelectorApp = FileSelectorApp()
    selected_file = fileSelectorApp.get_selected_file_name()
    print(f"Selected file: {os.path.abspath(selected_file)}")

    reader = XMLReader(os.path.abspath(selected_file))
    reader.load_xml()
    parsed_xml = reader.getParsedXML()
    print(parsed_xml)