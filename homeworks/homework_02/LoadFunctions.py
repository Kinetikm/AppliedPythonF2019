#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 18:53:58 2019

@author: altarion
"""


def maybe_json(f):
    import json
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError:
        data = None
    return data


def maybe_tsv(f):
    import csv
    try:
        data = csv.reader(f, delimiter='\t')
    except csv.Error:
        data = None
    return data


def try_print(parse_func, data):
    import DataBase
    try:
        base = parse_func(data)
        base.print_base()
    except DataBase.DataBaseError:
        print("Формат не валиден")


def check_encoding(path, encoding={"utf-8", "utf-16", "windows-1251"}):
    import chardet
    with open(f"{path}", "rb") as f:
        _data = f.read()
        _format = chardet.detect(_data)["encoding"]

    if _format not in encoding:
        print("Формат не валиден")
        return None, True
    return _format, False
