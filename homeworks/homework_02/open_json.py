#!/usr/bin/env python
# coding: utf-8


import json
import json_read
import open_tsv


def open_json_file(filename):
    try:
        with open(filename, encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            json_read.json_to_table(json_data)
    except UnicodeDecodeError:
        with open(filename, encoding='cp1251') as json_file:
            json_data = json.load(json_file)
            json_read.json_to_table(json_data)
