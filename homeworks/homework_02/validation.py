import json
from cerberus import Validator

from exceptions import ValidDataException
from schemas import DATA_SCHEMA


def check_json(file, encode):
    try:
        with open(file, encoding=encode) as read_file:
            json.load(read_file)
    except json.decoder.JSONDecodeError:
        return False

    return True


def check_schema(data):
    check_data = {"data": data}
    schema_validator = Validator(DATA_SCHEMA)
    if not schema_validator.validate(check_data):
        raise ValidDataException("Validation Error")
