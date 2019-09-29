import json
import csv
from io import StringIO


def read_json(text):
    try:
        text = json.loads(text)
        for i in range(len(text)):                # ints to strings
            for key in text[i]:
                if type(text[i][key]) == int:
                    text[i][key] = str(text[i][key])
    except Exception:
        return None
    return text


def read_csv(text):
    try:
        text = StringIO(text)
        lines = csv.DictReader(text, delimiter='\t', quotechar='\n')
        text = []
        for key in lines:
            text.append(dict(key))
    except Exception:
        return None
    return text
