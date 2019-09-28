# Cerberus schemas

# fmt: off

DATA_SCHEMA = {
    "data": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "Название": {
                    "type": "string",
                    "required": True
                },
                "Ссылка": {
                    "type": "string",
                    "required": True
                },
                "Теги": {
                    "type": "string",
                    "required": True
                },
                "Оценка": {
                    "type": "number",
                    "required": True
                },
            },
        },
    }
}

# fmt: on
