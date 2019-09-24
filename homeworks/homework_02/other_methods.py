#!/usr/bin/env python
# coding: utf-8


def json2lists(json_data):
    output = []
    output.append([key for key in json_data[0]])
    for dicts in json_data:
        output.append([dicts[key] for key in dicts])
    return output


def columns_len(data):
    output = []
    for i in range(len(data[0])):
        col_len = 0
        for lists in data:
            col_len = max(col_len, len(str(lists[i])))
        output.append(col_len)
    return output
