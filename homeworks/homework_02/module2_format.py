import json
import csv


def format_data(data, filename):
    # проверка что формат json
    try:
        json.loads(data)
        return 'json'
    except ValueError:
        result = 'no_json'
    #     проверка что формат tsv
    try:
        with open(filename) as f:
            csv.reader(filename, delimiter='\t')
        return 'tsv'
    except ValueError:
        result = 'no_json no_tsv'
    return result
