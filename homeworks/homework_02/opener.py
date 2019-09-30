import validator as val
import json


def json_open(file_name, encoding):
    with open(file_name, "r", encoding=encoding) as js:
        return json.load(js, object_hook=dict, parse_int=str)


def tsv_open(file_name, encoding):
    with open(file_name, 'r', encoding=encoding) as tsv:
        string = [i.split('\t') for i in tsv.read().split('\n')]
        dictionary = [{key: data for key, data in zip(string[0], string[k])} for k in range(1, len(string) - 1)]
        return dictionary


def json_tsv(file_name):
    encoding = val.check(file_name)
    if encoding is not None:
        try:
            return json_open(file_name, encoding)
        except Exception:
            return tsv_open(file_name, encoding)
    return None

