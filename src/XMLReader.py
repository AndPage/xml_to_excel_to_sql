import xml.etree.ElementTree as ET
import re


class XMLReader:
    params: list = ["id", "parent", "value", "source", "target"]
    relation_identifier = "source"
    file_path = None
    tree = None
    root = None
    parsed_xml: dict = {"entity": {}, "relation": []}

    def __init__(self, file_path):
        self.file_path = file_path

    def load_xml(self):
        self.tree = ET.parse(self.file_path)
        self.root = self.tree.getroot()

    def parse_xml(self):
        if self.root is None:
            raise Exception("XML not loaded. Call load_xml() first.")

        for mxCell in self.root.findall(".//mxCell"):
            item = {}
            for param in self.params:
                self.setByParamName(item, mxCell, param)

            if "parent" not in item or item["parent"] == 0:
                continue

            if self.relation_identifier in item:
                self.parsed_xml["relation"].append(item)
                continue

            parent_id = item["parent"]
            if parent_id == 1:
                parent_id = "table"
            if parent_id not in self.parsed_xml["entity"]:
                self.parsed_xml["entity"][parent_id] = []
            self.parsed_xml["entity"][parent_id].append(item)

    def setByParamName(self, dict: dict, cell, param: str):
        paramValue = cell.get(param)
        if paramValue is None:
            return

        paramValue = self.remove_html_tags(paramValue)

        if paramValue.isnumeric():
            paramValue = int(paramValue)

        dict[param] = paramValue

    def remove_html_tags(self, text):
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    def getParsedXML(self):
        self.parse_xml()
        return self.parsed_xml


if __name__ == "__main__":
    reader = XMLReader("/home/dev/projects/draw_io_to_sql/xml_files/test.drawio.xml")
    reader.load_xml()
    parsed_xml = reader.getParsedXML()
    tab = "  "

    for Key, items in parsed_xml.items():
        print(Key)
        if isinstance(items, list):
            for item in items:
                print(f"{tab}{item}")
        else:
            for Key2, item2 in items.items():
                print(f"{tab}{Key2}")
                for item in item2:
                    print(f"{tab}{tab}{item}")
