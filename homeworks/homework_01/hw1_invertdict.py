#!/usr/bin/env python
# coding: utf-8


def invert(dct, key, data):
    if isinstance(data, (list, tuple, set)):
        for x in data:
            invert(dct, key, x)
    else:
        if isinstance(dct.get(data), (tuple, list, set)):
            dct.get(data).append(key)
        elif dct.get(data) is None:
            dct[data] = key
        else:
            dct[data] = [dct.get(data), key]


def invert_dict(source_dict):
    res = {}
    if len(source_dict) == 0:
        return None
    for x in source_dict.keys():
        invert(res, x, source_dict.get(x))
    return res
