import re


class FieldTypeGenerator:
    true_string = "X"

    default_field_type = "VARCHAR(50)"
    field_type_pattern = {
        "DATE": [r'_at$', r'birthday', r'date', ],
        "INTEGER": [r'_id$', r'_id_dwh$', r'min$', r'max$', r'count$', r'_nr$', r'number$', r'year$', r'^day$', ],
        "TEXT": [r'comment', ],
        "REAL": [r'price', r'discount', r'percent', ],
        "VARCHAR(10)": [r'postal_code', ],
    }

    default_is_not_null = ""
    is_not_null_pattern = [
        r'name$',
        r'_id$',
    ]

    def get_field_type(self, field: str) -> str:
        for field_type, patterns in self.field_type_pattern.items():
            if any(re.search(pattern, field.lower()) for pattern in patterns):
                return field_type
        return self.default_field_type

    def get_is_not_null(self, field: str, ai: bool, ) -> str:
        if ai:
            return self.true_string

        for pattern in self.is_not_null_pattern:
            if re.search(pattern, field.lower()):
                return self.true_string

        return self.default_is_not_null
