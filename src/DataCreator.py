import itertools
from src.helper.FieldTypeGenerator import FieldTypeGenerator


class DataCreator:
    raw_data = None
    sequence = None
    table_pk = {}
    data_dictionary_table = []

    def __init__(self, sequence, raw_data):
        self.raw_data = raw_data
        self.sequence = sequence
        self.fieldTypeGenerator = FieldTypeGenerator()

        self.create_data_table()

    def create_data_table(self, ):
        for table_id in [element for sublist in self.sequence.values() for element in sublist]:
            table = next((i for i in self.raw_data["entity"]["table"] if i['id'] == table_id), None)
            if not table:
                print(f"Table {table_id} does not exist")
                continue
            table_name = table.get("value")
            tableRows = self.get_table_rows(table_id)

            for tableRow in tableRows:
                table_list = self.table_pk[table_id]
                pk = 'x' if tableRow in table_list["pk"] else ""
                fk = 'x' if tableRow in table_list["fk"] else ""
                ai = 'x' if tableRow in table_list["pk"] and len(table_list["pk"]) == 1 and "_id" in tableRow.lower() else ""
                field_type = self.fieldTypeGenerator.get_field_type(tableRow)
                self.data_dictionary_table.append({
                    "table": table_name,
                    "table_row": tableRow,
                    "field_type": field_type,
                    "pk": pk,
                    "ai": ai,
                    "fk": fk,
                    "not_null": tableRow,
                    "description": tableRow,
                })

            # import pandas as pd
            #
            # # Daten zeilenweise im Dictionary halten
            # data = [
            #     {'Name': 'Alice', 'Alter': 25, 'Stadt': 'Berlin'},
            #     {'Name': 'Bob', 'Alter': 30, 'Stadt': 'Hamburg'},
            #     {'Name': 'Charlie', 'Alter': 35, 'Stadt': 'München'}
            # ]
            #
            # # Erstelle ein DataFrame aus der Liste von Dictionaries
            # df = pd.DataFrame(data)
            #
            # # Schreibe das DataFrame in eine Excel-Datei
            # df.to_excel('daten_zeilenweise.xlsx', index=False)

    # def get_expanded_sequence(self):
    #     list(itertools.chain(*self.sequence))

    def get_table_rows(self, table_id) -> list:
        tableRow_list = []
        table_row_list = {"pk": [], "fk": []}
        for tableRow in [i for i in self.raw_data["entity"]["tableRow"] if i.get('parent') == table_id]:
            is_pk = False
            is_fk = False
            tableRow_string = []
            tableRow_id = tableRow.get("id")
            if "value" in tableRow and tableRow["value"] != '':
                if "_id_dwh" in str(tableRow["value"]).lower() or "(pk)" in str(tableRow["value"]).lower():
                    is_pk = True
                if "(fk)" in str(tableRow["value"]).lower():
                    is_fk = True
                tableRow_string.append(tableRow.get("value"))

            if 'partialRectangle' in self.raw_data["entity"]:
                cell = self.raw_data["entity"]["partialRectangle"]
                for partialRectangle in [i for i in cell if i.get('parent') == tableRow_id]:
                    if "value" in partialRectangle and partialRectangle["value"] != '':
                        if str(partialRectangle["value"]).lower() == 'pk':
                            is_pk = True
                            continue
                        if str(partialRectangle["value"]).lower() == 'fk':
                            is_fk = True
                            continue
                        if str(partialRectangle["value"]).lower() in ['fk/pk', 'fk\pk', 'fk|pk', 'pk/fk', 'pk|fk']:
                            is_pk = True
                            is_fk = True
                            continue
                        tableRow_string.append(partialRectangle.get("value"))
            row_string = ', '.join(tableRow_string)
            tableRow_list.append(row_string)

            if is_pk:
                table_row_list['pk'].append(row_string)
            if is_fk:
                table_row_list['fk'].append(row_string)

        self.table_pk[table_id] = table_row_list
        return tableRow_list

    def get_field_type(self, tableRow: str) -> str:
        return tableRow

    def get_table(self):
        for i in self.data_dictionary_table:
            print(i)

        return self.data_dictionary_table
