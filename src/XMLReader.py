import xml.etree.ElementTree as eT
import re


class XMLReader:
    params: list = ["id", "parent", "source", "target", "style", "value"]
    relation_identifier = "source"
    file_path = None
    tree = None
    root = None
    parsed_xml: dict = {"entity": {}, "relation": {}}

    def __init__(self, file_path):
        self.file_path = file_path

    def load_xml(self):
        self.tree = eT.parse(self.file_path)
        self.root = self.tree.getroot()

    def parse_xml(self):
        if self.root is None:
            raise Exception("XML not loaded. Call load_xml() first.")

        for mxCell in self.root.findall(".//mxCell"):
            element = {}
            for param in self.params:
                self.setByParamName(element, mxCell, param)

            if "parent" not in element or element["parent"] == 0:
                continue

            first_key = "entity"
            if element["style"] in ["rhombus", "triangle", "orthogonalEdgeStyle"]:
                first_key = "relation"

            key = element["style"]
            if key not in self.parsed_xml[first_key]:
                self.parsed_xml[first_key][key] = []
            self.parsed_xml[first_key][key].append(element)

    def setByParamName(self, element: dict, cell, param: str):
        paramValue = cell.get(param)
        if paramValue is None or paramValue == "":
            return

        paramValue = self.remove_html_tags(paramValue)

        if paramValue.isnumeric():
            paramValue = int(paramValue)

        if param == "style":
            paramValue = self.getShape(paramValue)

        element[param] = paramValue

    @staticmethod
    def remove_html_tags(text):
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    @staticmethod
    def getShape(string):
        shape = re.search(r"(\w+);", string).group(1)
        if shape == "text":
            shape = "tableRow"
        if shape == "swimlane":
            shape = "table"
        return shape

    def getParsedXML(self):
        self.parse_xml()
        return self.parsed_xml


if __name__ == "__main__":
    reader = XMLReader("/home/dev/projects/draw_io_to_sql/files/xml/test_snow.drawio.xml")
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
