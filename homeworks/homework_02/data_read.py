import json
import csv

from io import StringIO


def read_data(text):
    try:
        text = json.loads(text)
    except Exception:
        try:
            text = StringIO(text)
            reader = csv.DictReader(text, delimiter=",", quotechar='\n')
            text = []
            for line in reader:
                text.append(dict(line))
        except Exception:
            return None
    return text
