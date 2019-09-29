#!/usr/bin/env python
# coding: utf-8

"""
чтение и открытие
"""
import sys
import csv
from checkerror import *
import json
import shutil
from chardet.universaldetector import UniversalDetector


def define_coding(path):
    detector = UniversalDetector()
    with open(path, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']


# tsv
def open_tsv(filename, coding):
    with open(file=filename, mode='r', encoding=coding) as file:
        read = csv.reader(file, delimiter='\t')
        list = []
        column_num = 0
        for info in read:
            list.append(info)
        check_tsv(list)
        return list


# открываем json
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

# PATH = "C:\\Users\\User\\Desktop\\AppliedPythonF2019-homework_02
# \\homeworks\\homework_02\\files\\posts-cp1251.json"
# k = define_coding(PATH)
# print(k)
# print(type(k))
# for row in k:
#    print('{}\t{}\t{}'.format(row))
# print('*********')
