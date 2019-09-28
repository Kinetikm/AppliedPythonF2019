import json


def from_json(file, code):
    with open(file, encoding=code) as f:
        try:
            return json.load(f)
        except:
            return None
