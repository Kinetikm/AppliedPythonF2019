#!/usr/bin/env python
# coding: utf-8

import csv


def read(filename, encoding):
    data = []
    with open(filename, 'r', encoding=encoding) as f:
        raw = csv.reader(f, delimiter='\t')
        for item in raw:
            data.append(item)
    return data


def check(filename, encoding):
    with open(filename, 'r', encoding=encoding) as f:
        try:
            csv.reader(f, delimiter-'\t')
            return True
        except:
            return False
