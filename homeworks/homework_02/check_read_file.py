#!/usr/bin/env python
# coding: utf-8

import json
import csv


def json_check(filename, enc):
    with open(filename, 'r', encoding=enc) as f:
        try:
            json.load(f)
            return True
        except:
            return False


def tsv_check(filename, enc):
    with open(filename, 'r', encoding=enc) as f:
        try:
            csv.reader(f)
            return True
        except:
            return False


def json_read(filename, enc):
    result = []
    with open(filename, "r", encoding=enc) as f:
        data = json.load(f)
        result.append([i for i in data[0]])
        for dict in data:
            result.append([dict[i] for i in dict])
        return result


def tsv_read(filename, enc):
    result = []
    with open(filename, 'r', encoding=enc) as f:
        reader = csv.reader(f, delimiter='\t')
        for i in reader:
            result.append(i)
    return result
