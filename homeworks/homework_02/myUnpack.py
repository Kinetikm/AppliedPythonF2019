import json
import csv


def unpack(txt):
    try:
        unpck = json.loads(txt)
        for row in unpck:
            for _, value in row.items():
                if value is None:
                    return None
        return unpck
    except json.JSONDecodeError:
        try:
            txt = [i.split('\t') for i in txt.split('\n')]
            unpck = []
            clmns = len(txt[0])
            for i in range(1, len(txt) - 1):
                if clmns != len(txt[i]):
                    return None
                unpck.append({txt[0][name]: txt[i][name] for name in range(len(txt[0]))})
            return unpck
        except Exception as e:
            print(e)
            return None
