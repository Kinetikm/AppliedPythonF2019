#!/usr/bin/env python
# coding: utf-8


import csv
import json


def reading(file_name, check, enc):
    with open(file_name, 'r', encoding=enc) as f:
        if check == "json":
            reader = json.load(f)
        reader = csv.DictReader(f, delimiter='/t')
        return reader
