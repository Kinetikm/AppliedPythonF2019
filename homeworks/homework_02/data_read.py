import json
import csv

from io import StringIO


def read_data(text):
    try:
        text = json.loads(text)
    except Exception:
        try:
            text = StringIO(text)
            reader = csv.DictReader(text, delimiter='\t', quotechar='\n')
            text = []
            for row in reader:
                text.append(dict(row))
        except Exception:
            return None
    return text
