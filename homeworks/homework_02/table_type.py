import json
import csv


def json_or_csv(f, enc):
    m = 0
    try:
        file = open(f, encoding=enc)
        data = json.load(file)
        for i in data:
            if not (m == 0 or m == len(i)):
                return None
            m = len(i)
        return 'json'
    except:
        try:
            file = open(f, encoding=enc)
            data = csv.reader(file, delimiter="\t")
            for i in data:
                if not (m == 0 or m == len(i)):
                    return None
                m = len(i)
            return 'csv'
        except:
            raise