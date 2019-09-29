import json


def json_check(file, en):
    with open(file, 'r', encoding=en) as f:
        try:
            data = json.load(f)
            m = len(data[0])
            for i in data:
                if m != len(i):
                    return False
                m = len(i)
            return True
        except:
            return False


def json_read(file, en):
    result = []
    with open(file, "r", encoding=en) as f:
        data = json.load(f)
        res = []
        for i in data[0]:
            res.append(str(i))
        result.append(res)
        for k in range(len(data)):
            res = []
            for key in data[k]:
                res.append(str(data[k][key]))
            result.append(res)
        return result
