#!/usr/bin/env python
# coding: utf-8


import json
import csv
import encode_data


def open_tvs(file_name, encode):
    with open(file_name, "r", encoding=encode) as file:
        string = [x.split("\t") for x in file.read().split("\n")]
        res_dict = [{key: data for key, data in zip(string[0], string[j])}
                    for j in range(1, len(string) - 1)]
        return res_dict


def open_json(file_name, encode):
    with open(file_name, "r", encoding=encode) as file:
        return json.load(file, object_hook=dict, parse_int=str)


def open_file(file_name):
    encode = encode_data.encode_method(file_name)
    if encode is not None:
        try:
            return open_json(file_name, encode)
        except Exception:
            return open_tsv(file_name, encode)
    else:
        print("Формат не валиден")
