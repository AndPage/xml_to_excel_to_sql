import re


class DefaultGenerator:
    true_string = "X"

    default_field_type = "VARCHAR(64)"
    field_type_pattern = {
        "VARCHAR(10)": [r'^postal_code$', ],
        "TIMESTAMP": [r'_at$', r'birthday', r'date', r'^date_from$', r'^date_to$', r'^create_at$', r'^modify_at$', r'^ts_modify$', r'^ts_create$', ],
        "REAL": [r'price', r'discount', r'percent', ],
        "INTEGER": [r'_id$', r'_id_dwh$', r'_key$', r'_bk$', r'min$', r'max$', r'count$', r'_nr$', r'number$', r'year$', r'^day$', ],
        "TEXT": [r'comment', r'description', ],
    }

    default_is_not_null = ""
    is_not_null_pattern = [
        r'name$',
        r'_id$',
        r'_hk$',
        r'_key$',
        r'_id_dwh$',
    ]

    default_optional = ""
    default_date_to = "9999-12-31 00:00:00"
    is_optional_pattern = {
        "DEFAULT CURRENT_TIMESTAMP": [r'^create_at$', r'^modify_at$', r'^date_from$', r'^ts_create$', r'^ts_modify$', ]
    }

    table_name_prefixes = [
        "tb_dim_",
        "tb_facts_",
        "tb_hub_",
        "tb_link_",
        "tb_sat_",
        "tb_",
    ]

    column_names = {
        "create_at": "create date",
        "modify_at": "last modify date",
        "date_from": "validity start",
        "date_to": "validity end",
    }

    def get_field_type(self, field: str) -> str:
        for field_type, patterns in self.field_type_pattern.items():
            if any(re.search(pattern, field.lower()) for pattern in patterns):
                return field_type

        return self.default_field_type

    def get_is_not_null(self, field: str) -> str:
        for pattern in self.is_not_null_pattern:
            if re.search(pattern, field.lower()):
                return self.true_string

        return self.default_is_not_null

    def get_optional(self, field):
        if field == "date_to":
            return f"DEFAULT '{self.default_date_to}'"

        for optional, patterns in self.is_optional_pattern.items():
            if any(re.search(pattern, field.lower()) for pattern in patterns):
                return optional

        return self.default_optional

    def get_clear_table_name(self, table_name):
        for prefix in self.table_name_prefixes:
            if table_name.startswith(prefix):
                return table_name.removeprefix(prefix)

        return table_name

    def get_description(self, tableRow, table_name):
        table_clear_name = self.get_clear_table_name(table_name)
        for pattern, replacement in self.column_names.items():
            if re.search(pattern, tableRow.lower()):
                tableRow = replacement
            if table_clear_name in tableRow:
                tableRow = tableRow.replace(table_clear_name, "")

        return f"{tableRow.replace('_', ' ').replace('  ', ' ').strip()} of the {table_clear_name.replace('_', ' ')}"

    def is_dwh(self, table):
        for prefix in self.table_name_prefixes[:-1]:
            if table.startswith(prefix):
                return True
        return False
