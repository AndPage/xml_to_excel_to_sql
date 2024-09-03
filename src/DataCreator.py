from src.helper.FieldTypeGenerator import FieldTypeGenerator
from src.helper.RelationsFormatter import RelationsFormatter


class DataCreator:
    raw_data = None
    sequence = None
    relations = None
    table_pk = {}
    data_dictionary_table = []

    def __init__(self, sequence, raw_data):
        self.relations = RelationsFormatter(raw_data).get_formatted_relations()
        self.raw_data = raw_data
        self.sequence = sequence
        self.fTG = FieldTypeGenerator()

        self.create_data_table()

    def create_data_table(self, ):
        for table_id in [element for sublist in self.sequence.values() for element in sublist]:
            table = next((i for i in self.raw_data["entity"]["table"] if i['id'] == table_id), None)
            if not table:
                print(f"Table {table_id} does not exist")
                continue
            table_name = table.get("value")
            tableRows = self.get_table_rows(table_id, table['value'])

            for tableRow in tableRows:
                table_list = self.table_pk[table_id]
                pk = self.fTG.true_string if tableRow in table_list["pk"] else ""
                fk = self.get_fk(tableRow, table_list, table_id)
                ai = self.fTG.true_string if tableRow in table_list["pk"] and len(
                    table_list["pk"]) == 1 and "_id" in tableRow.lower() else ""
                field_type = self.fTG.get_field_type(tableRow)
                not_null = self.fTG.get_is_not_null(tableRow, ai == self.fTG.true_string)
                self.data_dictionary_table.append({
                    "table": table_name,
                    "table_row": tableRow,
                    "field_type": field_type,
                    "pk": pk,
                    "ai": ai,
                    "fk": fk,
                    "not_null": not_null,
                    "description": f"{tableRow.replace('_', ' ')} of the {table_name.removeprefix('tb_')}",
                })

    def get_table_rows(self, table_id, table) -> list:
        tableRow_list = []
        table_row_list = {"pk": [], "fk": [], "name": table}
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
                        cell_str = str(partialRectangle["value"]).lower().strip()
                        if cell_str == 'pk':
                            is_pk = True
                            continue
                        if cell_str == 'fk':
                            is_fk = True
                            continue
                        if cell_str in ['fk/pk', 'fk|pk', 'pk/fk', 'pk|fk']:
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

    def get_fk(self, tableRow, table_list, table_id):
        if tableRow in table_list["fk"]:
            possible_source_ids = [i['source'] for i in self.relations if i['target'] == table_id]
            possible_source_table = [self.table_pk[key] for key in possible_source_ids if key in self.table_pk]
            table = (next((i for i in possible_source_table if any(s.lower() in tableRow.lower() for s in i['pk'])), None))

            if table:
                return self.fk_from_table(table)

            print(f"Table Name does not exist\n"
                  f"tableRow.lower(): {tableRow.lower()}\n"
                  f"tableRow.lower().removesuffix('_id') next try: {tableRow.lower().removesuffix('_id')}\n"
                  f"possible_source_ids: {possible_source_ids}\n"
                  f"possible_source_table: {possible_source_table}"
                  )
            table = (next((i for i in possible_source_table if any(s.lower() in tableRow.lower().removesuffix("_id") for s in i['pk'])), None))
            if table:
                print(f"second attempt worked\n{tableRow.lower().removesuffix('_id')} => {table['pk'](0)}")
                return self.fk_from_table(table)

            print(f"Table Name does not exist\n")
            return self.fTG.true_string
        return ""

    @staticmethod
    def fk_from_table(table: dict) -> str:
        print(table)
        return f"{table['name']}({table['pk'][0]})"

    def get_table(self):
        for i in self.data_dictionary_table:
            print(i)

        return self.data_dictionary_table
