#!/usr/bin/env python
# coding: utf-8


import csv
import json


def checking(file_name, enc):
    try:
        with open(file_name, 'r', encoding=enc) as f:
            f.loads()
            return "json"
    except:
        with open(file_name, 'r', encoding=enc) as f:
            f.read()
            return "csv"
    return "Файл не валиден"
