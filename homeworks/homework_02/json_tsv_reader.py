import csv
import json


def extract_data(data):
    try:
        json_data = json.loads(data)
        rows = list()
        header = tuple(json_data[0].keys())
        for block in json_data:
            row = []
            for i, name in enumerate(header):
                row.append(block[name])
            rows.append(tuple(row))
        return 0, header, rows
    except json.JSONDecodeError:
        try:
            reader = csv.reader(data.strip("\n").split("\n"), delimiter='\t')
            header = []
            rows = []
            for i, line in enumerate(reader):
                if not i:
                    header = tuple(line)
                else:
                    rows.append(tuple(line))
            return 0, header, rows
        except csv.Error:
            return 1, None, None
    except AttributeError:
        return 1, None, None
