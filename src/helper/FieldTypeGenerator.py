import re


class FieldTypeGenerator:
    default_type = "VARCHAR(50)"
    pattern = {
        "INTEGER": [r'_id$', r'_id_dwh$', r'min', r'max', r'count', r'_nr', r'number', r'year', r'month', r'day', ],
        "TEXT": [r'comment', ],
        "REAL": [r'price', r'discount', r'percent', ],
        "DATE": [r'_at$', r'birthday', r'price', ],
        "VARCHAR(10)": [r'postal_code', ],
    }

    def get_field_type(self, field: str) -> str:
        for field_type, patterns in self.pattern.items():
            if any(re.search(pattern, field.lower()) for pattern in patterns):
                return field_type
        return self.default_type
