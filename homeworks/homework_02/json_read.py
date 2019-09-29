import json


def json_check(file, en):
    with open(file, 'r', encoding=en) as f:
        try:
            json.load(f)
            return True
        except:
            return False


def json_read(file, en):
    result = []
    with open(file, "r", encoding=en) as f:
        data = json.load(f)
        res = []
        for i in data[0]:
            res.append(i)
        result.append(res)
        for k in range(len(data)):
            res = []
            for key in data[k]:
                res.append(data[k][key])
            result.append(res)
        return result
