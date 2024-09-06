from src.helper.DefaultGenerator import DefaultGenerator
import copy


class SqlCreator:
    data_list: list = []
    sql_data: list = []
    table_special: dict = {}
    special_raw: dict = {'pk': [], 'fk': [], 'date_to': False, 'modify_at': False}
    tab: str = "\t"

    def __init__(self, data_list):
        self.data_list = data_list
        self.dg = DefaultGenerator()

    def set_sql_data(self):
        table = self.data_list[0]["table"]
        # self.table_special[table] = {'pk': [], 'fk': [], 'date_to': False, 'modify_at': False}
        self.table_special[table] = copy.deepcopy(self.special_raw)
        self.start_table(table)

        for i, row in enumerate(self.data_list):
            if table != row["table"]:
                self.end_table(table)
                table = row["table"]
                # self.table_special[table] = {'pk': [], 'fk': [], 'date_to': False, 'modify_at': False}
                self.table_special[table] = copy.deepcopy(self.special_raw)
                self.start_table(table)

            if row['pk'].lower() == 'x' and 'x' != row["ai"].lower():
                self.table_special[table]['pk'].append(row['table_row'])
            if row['fk'].lower() != '':
                self.table_special[table]['fk'].append({'row': row['table_row'], 'ref': row['fk']})
            if row['table_row'].lower() == 'date_to':
                self.table_special[table]['date_to'] = True
            if row['table_row'].lower() == 'modify_at':
                self.table_special[table]['modify_at'] = True

            ai_val = " PRIMARY KEY AUTOINCREMENT" if row['pk'].lower() == 'x' and 'x' == row["ai"].lower() else ''
            nn_val = " NOT NULL" if 'x' == row["not_null"].lower() else ''
            optional = f" {row['optional']}" if row['optional'] != '' else ''
            self.sql_data.append(f"{self.tab}{row['table_row'].split(' ', 1)[0]} {row['field_type']}{ai_val}{nn_val}{optional},")

        self.end_table(table)

    def start_table(self, table):
        self.sql_data.append(f"DROP TABLE if EXISTS {table};")
        self.sql_data.append(f"CREATE TABLE {table}")
        self.sql_data.append(f"(")

    def end_table(self, table):
        if len(self.table_special[table]["pk"]) > 1:
            self.sql_data.append(f"{self.tab}PRIMARY KEY ({", ".join(self.table_special[table]["pk"])}),")

        for fk in self.table_special[table]["fk"]:
            self.sql_data.append(f"{self.tab}FOREIGN KEY ({fk['row']}) REFERENCES {fk['ref']},")

        self.sql_data[-1] = self.sql_data[-1].rstrip(",")
        self.sql_data.append(");")
        self.sql_data.append("")

        table_clear_name = self.dg.get_clear_table_name(table)
        if self.table_special[table]['date_to']:
            self.trigger_date_to(table, table_clear_name)
        if self.table_special[table]['modify_at']:
            self.trigger_modify_at(table, table_clear_name)

    def trigger_modify_at(self, table, table_clear_name):
        self.sql_data.append(f"CREATE TRIGGER IF NOT EXISTS update_modify_at_{table}")
        self.sql_data.append(f"{self.tab}AFTER UPDATE ON {table}")
        self.sql_data.append(f"{self.tab}FOR EACH ROW")
        self.sql_data.append(f"{self.tab}WHEN (SELECT COUNT(*) FROM pragma_table_info('{table}') WHERE name = 'modify_at') > 0")
        self.sql_data.append(f"BEGIN")
        self.sql_data.append(f"{self.tab}UPDATE {table} SET modify_at = CURRENT_TIMESTAMP WHERE {table_clear_name}_id = OLD.{table_clear_name}_id;")
        self.sql_data.append(f"END;")
        self.sql_data.append(f"")

    def trigger_date_to(self, table, table_clear_name):
        self.sql_data.append(f"CREATE TRIGGER IF NOT EXISTS update_date_to_{table}")
        self.sql_data.append(f"{self.tab}AFTER INSERT ON {table}")
        self.sql_data.append(f"{self.tab}FOR EACH ROW")
        self.sql_data.append(f"{self.tab}WHEN (SELECT COUNT(*)")
        self.sql_data.append(f"{self.tab}{self.tab}FROM pragma_table_info('{table}')")
        self.sql_data.append(f"{self.tab}{self.tab}WHERE name = 'os_{table_clear_name}_key' > 0")
        self.sql_data.append(f"{self.tab}{self.tab}AND name = 'date_to' > 0)")
        self.sql_data.append(f"BEGIN")
        self.sql_data.append(f"{self.tab}UPDATE {table}")
        self.sql_data.append(f"{self.tab}SET date_to = CURRENT_TIMESTAMP")
        self.sql_data.append(f"{self.tab}WHERE os_{table_clear_name}_key = NEW.os_{table_clear_name}_key")
        self.sql_data.append(f"{self.tab}AND date_to = '{self.dg.default_date_to}';")
        # self.sql_data.append(f"{self.tab}LIMIT 1;") # LIMIT wird von SQLite nicht unterstützt, alternative bei grosser Datenbank nötig
        self.sql_data.append(f"END;")
        self.sql_data.append(f"")

    def get_sql_data(self):
        self.set_sql_data()
        for i in self.sql_data:
            print(i)

        return self.sql_data
