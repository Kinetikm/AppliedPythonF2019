#!/usr/bin/env python
# coding: utf-8


import sys
import csv
from error import *
import json
import shutil
from chardet.universaldetector import UniversalDetector


def define_coding(path):
    detect = UniversalDetector()
    with open(path, 'rb') as fh:
        for line in fh:
            detect.feed(line)
            if detect.done:
                break
        detect.close()
    return detect.result['encoding']


def open_tsv(filename, coding):
    with open(file=filename, mode='r', encoding=coding) as file:
        read = csv.reader(file, delimiter='\t')
        list = []
        for info in read:
            list.append(info)
        check_tsv(list)
        return list


def open_json(filename, coding):
    with open(file=filename, mode='r', encoding=coding) as file:
        list = json.load(file)
    check_json(list)
    return list


def data(filename, coding):
    try:
        return open_json(filename, coding)
    except json.decoder.JSONDecodeError:
        return open_tsv(filename, coding)
