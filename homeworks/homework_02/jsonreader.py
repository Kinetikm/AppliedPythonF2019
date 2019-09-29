#!/usr/bin/env python
# coding: utf-8

import json


def read(filename, encoding):
    data = []
    with open(filename, 'r', encoding=encoding) as f:
        raw = json.load(f)
        data.append([key for key in raw[0]])
        for key in raw:
            data.append(key[value] for value in key)
    return data


def check(filename, encoding):
    try:
        with open(filename, 'r', encoding=encoding) as f:
            json.load(f)
        return True
    except:
        return False
