#!/usr/bin/env python
# coding: utf-8

import sys
from read_json import json_read, json_check
from read_tsv import tsv_read, tsv_check
import table_plus


class MyException(Exception):
    def __init__(self, text):
        self.txt = text

if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        file = open(filename, "r")
        enc = table_plus.enc_detect(filename)
        file.close()

        if enc not in {'utf-8', 'utf-16', 'windows-1251'}:
            raise MyException("Формат не валиден")
        form = json_check(filename, enc)
        if form != 'json':
            form = tsv_check(filename, enc)
            if form != 'tsv':
                raise MyException("Формат не валиден")
            else:
                data = tsv_read(filename, enc)
        else:
            data = json_read(filename, enc)
        table_plus.check_data(data)
        table_plus.print_table(data, table_plus.len_of_str(data))
    except FileNotFoundError:
        print("Файл не валиден")
    except MyException as ex:
        print(ex)
