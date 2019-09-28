#!/usr/bin/env python
# coding: utf-8


import csv
import json
import encode_data as ecd


def open_js(file_name, encode):
    with open(file_name, "r", encoding=encode) as file:
        return json.load(file, object_hook=dict, parse_int=str)


def open_tvs(file_name, encode):
    with open(file_name, "r", encoding=encode) as file:
        string = [i.split("\t") for i in file.read().split("\n")]
        res_dict = [{key: data for key, data in zip(string[0], string[j])}
                    for j in range(1, len(string) - 1)]
        return res_dict


def open_data(file_name):
    encode = ecd.ch_encod(file_name)
    if encode is not None:
        try:
            return open_js(file_name, encode)
        except Exception:
            return open_tsv(file_name, encode)
    else:
        print('Формат не валиден')
<<<<<<< HEAD
=======
        
>>>>>>> 2f3e70e52e3709cbf5e4e83293797ff942d3925f
