#!/usr/bin/env python
# coding: utf-8


import json
import csv


def json_reading(f):
    try:
        info = json.load(f)
        columns = list(info[0].keys())
        result = [columns]
        for item in info:
            result.append([item[key] for key in columns])
        return result
    except json.JSONDecodeError:
        return None


def tsv_reading(f):
    try:
        dialect = csv.Sniffer().sniff(f.read(1024), delimiters="\t")
        reader = csv.reader(f, dialect=dialect)
        info = [line for line in reader]
        return info
    except csv.Error:
        return None
