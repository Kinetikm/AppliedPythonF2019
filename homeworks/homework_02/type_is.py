import json
import csv


def json_or_csv(f, enc):
    l = 0
    try:
        file = open(f, encoding=enc)
        data = json.load(file)
        for i in data:
            if not (l == 0 or l == len(i)):
                return None
            l = len(i)
        return 'json'
    except:
        try:
            file = open(f, encoding=enc)
            data = csv.reader(file, delimiter="\t")
            for i in data:
                if not (l == 0 or l == len(i)):
                    return None
                l = len(i)
            return 'csv'
        except:
            raise
