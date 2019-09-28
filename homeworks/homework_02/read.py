import json
import tsv


def isjson(path, enc):
    try:
        with open(path, encoding=enc) as f:
            d = json.load(f)
    except json.decoder.JSONDecodeError:
        return False
    else:
        return True


def read_file(path, enc)->list:
    A = []
    if isjson(path, enc):
        with open(path, encoding=enc) as f:
            d = json.load(f)
        A.append(list(d[0].keys()))
        for line in d:
            A.append(list(line.values()))
        A = [list(map(str, item)) for item in A]
    else:
        with open(path, encoding=enc) as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            for row in tsvreader:
                A.append(row)
    return(A)
