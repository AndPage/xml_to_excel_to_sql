import re


class InsertCreator:
    sql_data: list = []
    sql_data_dict: dict = {}
    substr1: str = "XXX"
    data_field: str = "YYY"
    tab: str = "\t"
    block_size = 1000
    counter: int = 0

    def __init__(self, data_list: dict):
        self.data_list: dict = data_list

    def set_sql_data(self):
        for table_name, value_list in self.data_list.items():
            for i in range(0, len(value_list), self.block_size):
                self.start_insert(table_name, value_list[i])
                for value in value_list[i:i + self.block_size]:
                    self.insert_values(value)
                self.end_insert(table_name)

    def insert_values(self, values: dict):
        insert_values = []
        for key, value in values.items():
            if key == self.data_field:
                continue

            if len(key.split(" ")) == 1:
                insert_values.append(f'"{value}"')
                continue

            val: str = key
            if self.substr1.upper() in val.upper():
                val = re.sub(f"'{self.substr1}'", f'"{value}"', val, flags=re.IGNORECASE)
                val = re.sub(self.substr1, value, val, flags=re.IGNORECASE)
                # val = val.replace(self.substr1, value)

            if self.data_field.upper() in val.upper():
                val = re.sub(f"'{self.data_field}'", f'"{values[self.data_field]}"', val, flags=re.IGNORECASE)
                val = re.sub(self.data_field, values[self.data_field], val, flags=re.IGNORECASE)
                # val = val.replace(self.data_field, values[self.data_field])

            insert_values.append(f"(SELECT {val})")

        self.sql_data.append(f"{self.tab}({', '.join(insert_values)}),")

    def start_insert(self, table, value):
        columns = [s.split(' ', 1)[0] for s in value.keys() if s != self.data_field]
        self.sql_data.append(f"INSERT INTO {table} ({', '.join(columns)})")
        self.sql_data.append("VALUES")

    def end_insert(self, table_name: str):
        self.sql_data[-1] = f"{self.sql_data[-1].rstrip(",")};"
        self.sql_data_dict[f"{str(self.counter).zfill(3)}_{table_name.removeprefix('tb_')}"] = self.sql_data
        self.sql_data = []
        self.counter += 1

    def get_sql_data(self) -> dict:
        self.set_sql_data()
        # for i in self.sql_data:
        #     print(i)

        return self.sql_data_dict
