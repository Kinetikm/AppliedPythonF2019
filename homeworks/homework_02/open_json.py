#!/usr/bin/env python
# coding: utf-8


import json
import json_read
import open_tsv


def json_func(filename, using_code):
    with open(filename, encoding=using_code) as json_file:
        json_data = json.load(json_file)
        json_read.json_to_table(json_data)


def open_json_file(filename):
    try:
        json_func(filename, 'utf-8')
    except UnicodeDecodeError:
        try:
            json_func(filename, 'utf-16')
        except UnicodeDecodeError:
            json_func(filename, 'cp1251')
