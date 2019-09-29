import csv
import json


def read(text):
    try:
        json_text = json.loads(text)
        rows = list()
        title = tuple(json_text[0].keys())
        for block in json_text:
            row = list()
            for i, name in enumerate(title):
                row.append(block[name])
            rows.append(tuple(row))
        return 0, title, rows
    except json.JSONDecodeError:
        try:
            data = csv.reader(text.strip("\n").split("\n"), delimiter='\t')
            # type(data) => list()
            title = list()
            rows = list()
            for i, line in enumerate(data):
                if i == 0:
                    title = tuple(line)
                else:
                    rows.append(tuple(line))
            return 0, title, rows
        except csv.Error:
            return 1, None, None
    except AttributeError:
        return 1, None, None
