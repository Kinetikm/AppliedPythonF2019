import json


def json_check(file, en):
    with open(file, 'r', encoding=en) as f:
        try:
            json.load(f)
            return True
        except:
            return False


def json_read(file, en):
    with open(file, "r", encoding=en):
        data = json.load(file)
        return data
