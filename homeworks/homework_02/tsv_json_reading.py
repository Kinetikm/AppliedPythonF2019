import json
import csv


def file_to_data(file):
    try:
        data = json.loads(file)
        rows = list()
        header = tuple(file[0].keys())
        for now in data:
            row = []
            for i, elem in enumerate(header):
                row.append(now[elem])
            rows.append(tuple(row))
        return 0, header, rows
    except json.JSONDecodeError:
        try:
            reader = csv.reader(file.strip('\n').split('\n'), delimiter='\t')
            header = []
            rows = []
            for i, row in enumerate(reader):
                if not i:
                    header = tuple(row)
                else:
                    rows.append(tuple(row))
            return 0, header, rows
        except csv.Error:
            return 1, None, None
    except AttributeError:
        return 1, None, None
