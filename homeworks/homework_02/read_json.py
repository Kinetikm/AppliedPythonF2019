#!/usr/bin/env python
# coding: utf-8

import json


def json_read(filename, enc):
    jdata = []
    with open(filename, "r", encoding=enc) as file:
        data = json.load(file)
        jdata.append([key for key in data[0]])
        for dct in data:
            jdata.append([dct[item] for item in dct])
    return jdata


def json_check(filename, enc):
        try:
            with open(filename, 'r', encoding=enc) as file:
                json.load(file)
            return 'json'
        except:
            return "Формат не валиден"
