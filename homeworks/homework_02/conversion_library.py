#!/usr/bin/env python
# coding: utf-8

import csv
import json
from encoding_library import find_encoding


def conversion_to_columns(strings):
    columns = [0] * len(strings[0])
    for i in range(len(columns)):
        columns[i] = []

    for x in strings:
        for i in range(len(strings[0])):
            columns[i].append(x[i])

    return columns


def strings_tsv(file_name):
    with open(file_name, encoding=find_encoding(file_name)) as file:
        file_data = csv.reader(file, delimiter="\t")

        strings = []
        for line in file_data:
            strings.append(line)

    return strings


def strings_json(file_name):
    with open(file_name, encoding=find_encoding(file_name)) as file:
        file_data = json.load(file)

    strings = [0] * (len(file_data) + 1)
    for i in range(len(strings)):
        strings[i] = []

    for x in file_data[0].keys():
        if isinstance(x, str):
            strings[0].append(x)
        else:
            x = str(x)
            strings[0].append(x)

    for i in range(len(file_data)):
        for x in file_data[i].values():
            if isinstance(x, str):
                strings[i + 1].append(x)
            else:
                x = str(x)
                strings[i + 1].append(x)

    return strings
