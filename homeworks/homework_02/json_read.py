#!/usr/bin/env python
# coding: utf-8

import json


def json_check(path_2_file, enc):
    with open(path_2_file, 'r', encoding=enc) as f:
        try:
            json.load(f)
            return True
        except:
            return False


def json_read(path_2_file, enc):
    result = []
    with open(path_2_file, "r", encoding=enc) as f:
        data = json.load(f)
        result.append([i for i in data[0]])
        for dict in data:
            result.append([dict[i] for i in dict])
        return result
