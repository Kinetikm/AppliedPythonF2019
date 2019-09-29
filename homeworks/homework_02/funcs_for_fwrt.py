def det_file_encoding(filename):
    encodings = ['utf-8', 'cp1251', 'utf16']
    for e in encodings:
        try:
            with open(filename, 'r',
                      encoding=e) as f:
                f.read()
        except UnicodeDecodeError:
            pass
        else:
            enc = e
            break
    return enc


def parse_json(jsondata):
    data = []
    headers = list(jsondata[0].keys())
    data.append(headers)
    for dicts in jsondata:
        data.append(list(dicts.values()))
    return data


def csv_validation(data):
    length = max([len(i) for i in data])
    for line in data:
        if length != len(line):
            return False
    return True
