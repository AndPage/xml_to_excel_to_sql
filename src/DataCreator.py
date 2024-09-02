import itertools


class DataCreator:
    raw_data = None
    sequence = None
    table_pk = []
    data_dictionary_table = []

    def __init__(self, sequence, raw_data):
        self.raw_data = raw_data
        self.sequence = sequence
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
                self.data_dictionary_table.append({
                    "table": table_name,
                    "table_row": tableRow,
                    "field_type": tableRow,
                    "pk": tableRow,
                    "ai": tableRow,
                    "fk": tableRow,
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

    def get_table_rows(self, table_id)->list:
        tableRow_list = []
        for tableRow in [i for i in self.raw_data["entity"]["tableRow"] if i.get('parent') == table_id]:
            is_pk = False
            is_fk = False
            tableRow_id = tableRow.get("id")
            if "value" in tableRow and tableRow["value"] != '':
                if "(pk)" in str(tableRow["value"]).lower():
                    is_pk = True
                if "(fk)" in str(tableRow["value"]).lower():
                    is_fk = True
                tableRow_list.append(tableRow.get("value"))

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
                        tableRow_list.append(partialRectangle.get("value"))

        return tableRow_list

    def get_table(self):
        for i in self.data_dictionary_table:
            print(i)

        return self.data_dictionary_table

