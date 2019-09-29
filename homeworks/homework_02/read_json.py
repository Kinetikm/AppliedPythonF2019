import json


def read_json(filename, e):
    with open(filename, "r", encoding=e) as f:
        temp = json.load(f)
        output = {}
        for k in temp[0].keys():
            output[k] = []
        for row in temp[1:len(temp)]:
            for k in row.keys():
                output[k].append(row[k])
        return output

