#!/usr/bin/env python
# coding: utf-8


import csv
import json
import encode as ecd


def read_jfile(file_name, encode):
    with open(file_name, "r", encoding=encode) as file:
        return json.load(file, object_hook=dict, parse_int=str)


def read_tfile(file_name, encode):
    with open(file_name, "r", encoding=encode) as file:
        str = [i.split("\t") for i in file.read().split("\n")]
        ret = [{key: data for key, data in zip(str[0], str[j])}
            for j in range(1, len(str) - 1)]
        return ret


def open_data(file_name):
    encode = ecd.ch_encod(file_name)
    if encode is not None:
        try:
            return read_file(file_name, encode)
        except Exception:
            return read_tfile(file_name, encode)
    else:
        print('Формат не валиден')
