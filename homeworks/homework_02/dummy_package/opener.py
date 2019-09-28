from dummy_package import validator as vd
import json


def open_like_json(file_name, encode):
    with open(file_name, "r", encoding=encode) as json_file:
        return json.load(json_file, object_hook=dict, parse_int=str)


def open_like_tsv(file_name, encode):
    with open(file_name, "r", encoding=encode) as tsv_file:
        string = [i.split("\t") for i in tsv_file.read().split("\n")]
        ret_dict = [{key: data for key, data in zip(string[0], string[j])}
                    for j in range(1, len(string) - 1)]
        return ret_dict


def json_or_tsv(file_name):
    encode = vd.check_encode(file_name)
    if encode is not None:
        try:
            return open_like_json(file_name, encode)
        except Exception:
            return open_like_tsv(file_name, encode)
    return None
