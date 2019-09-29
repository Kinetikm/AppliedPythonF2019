#!/usr/bin/env python
# coding: utf-8


def data_to_json(data):
    lines = data.split("\n")
    output_list = []
    a = {}
    if lines[0] != "":
        keys = lines[0].split("\t")
    length = len(keys)
    for i in range(1, len(lines)-1):
        line = lines[i]
        line_list = line.split("\t")
        if len(line_list) != length or line_list[0] == "":
            return False
        a = {keys[0]: line_list[0],
             keys[1]: line_list[1],
             keys[2]: line_list[2],
             keys[3]: line_list[3]
             }
        output_list.append(a)
    return output_list, keys


def check_data(data, keys=[], json_status=False):
    if not json_status:
        if data == "file_not_found":
            print("Файл не валиден")
            return False
        elif not data:
            print("Формат не валиден")
            return False
        else:
            return True
    else:
        for var in data:
            if list(var.keys()) != keys:
                print("Формат не валиден")
                return False
    return True
