class SqlCreator:
    data_list: list = []
    sql_data: list = []
    table_special: dict = {}
    tab: str = "\t"

    def __init__(self, data_list):
        self.data_list = data_list

    def set_sql_data(self):
        table = self.data_list[0]["table"]
        self.table_special[table] = {'pk': [], 'fk': []}
        self.set_start_sql_data()

        for i, row in enumerate(self.data_list):
            if table != row["table"]:
                self.end_table(table)
                table = row["table"]
                self.table_special[table] = {'pk': [], 'fk': []}
                self.start_table(table)

            if row['pk'].lower() == 'x' and 'x' != row["ai"].lower():
                self.table_special[table]['pk'].append(row['table_row'])
            if row['fk'].lower() != '':
                self.table_special[table]['fk'].append({'row': row['table_row'], 'ref': row['fk']})

            ai_val = " PRIMARY KEY AUTOINCREMENT" if row['pk'].lower() == 'x' and 'x' == row["ai"].lower() else ''
            nn_val = " NOT NULL" if 'x' == row["not_null"].lower() else ''
            sep = self.get_sep(table,i)
            self.sql_data.append(f"{self.tab}{row['table_row']} {row['field_type']}{ai_val}{nn_val}{sep}")
        self.end_table(table)

    def set_start_sql_data(self):
        self.start_table(self.data_list[0]["table"])

    def start_table(self, table):
        self.sql_data.append(f"DROP TABLE if EXISTS {table};")
        self.sql_data.append(f"CREATE TABLE {table}")
        self.sql_data.append(f"(")

    def end_table(self, table):
        next_value_available = ","
        sep = next_value_available if len(self.table_special[table]['fk']) else ''

        if len(self.table_special[table]["pk"]) > 1:
            self.sql_data.append(f"{self.tab}PRIMARY KEY ({", ".join(self.table_special[table]["pk"])}){sep}")

        if sep == next_value_available:
            for i, fk in enumerate(self.table_special[table]["fk"]):
                sep_fk = '' if i == len(self.table_special[table]["fk"]) - 1 else next_value_available
                self.sql_data.append(f"{self.tab}FOREIGN KEY ({fk['row']}) REFERENCES {fk['ref']}{sep_fk}")
        self.sql_data.append(");")
        self.sql_data.append("")

    def get_sep(self, table,i):
        not_last_attribute_in_table = i + 1 < len(self.data_list) and table == self.data_list[i + 1]["table"]
        not_last_element_in_create = len(self.table_special[table]['fk']) or len(self.table_special[table]['pk'])

        return "," if not_last_attribute_in_table or not_last_element_in_create else''

    def get_sql_data(self):
        self.set_sql_data()
        for i in self.sql_data:
            print(i)

        return self.sql_data
