import json
import csv


def json_or_csv(f, enc):
    try:
        file = open(f, encoding=enc)
        data = json.load(file)
        return 'json'
    except:
        try:
            file = open(f, encoding=enc)
            data = csv.reader(file, delimiter="\t")
            return 'csv'
        except:
            raise
