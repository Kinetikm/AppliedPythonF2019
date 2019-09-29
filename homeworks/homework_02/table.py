#!/usr/bin/env python
# coding: utf-8


import sys

from det_enc import det_enc
from check_read_file import json_check, tsv_check, tsv_read, json_read
from terminaltables import AsciiTable


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename, "r")
        f.close()
    except:
        print('Файл не валиден')
        sys.exit()
    enc = det_enc(filename)
    if enc not in ['utf-8', 'utf-16', 'windows-1251', 'acsii']:
        print('Формат не валиден')
        sys.exit()
    if json_check(filename, enc):
        tablee = AsciiTable(json_read(filename, enc))
    elif tsv_check(filename, enc):
        tablee = AsciiTable(tsv_read(filename, enc))
        print(tablee.table)
