# -*- coding: utf-8 -*-

import json


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def json_data(json_file, cod):
    file = open(json_file, 'r', encoding=cod)

    if not is_json(file.read()):
        raise TypeError
    file.close()

    file = open(json_file, 'r', encoding=cod)

    data = json.load(file)
    file.close()
    return data
