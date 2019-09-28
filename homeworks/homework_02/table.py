#!/usr/bin/env python
# coding: utf-8

import sys

from gtable import GoodTable
from methods import json_to_list, tsv_to_list
from reading import read_file


class MyException(Exception):
    pass

if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        data, flag_json = read_file(filename)
        if flag_json:
            data = json_to_list(data)
        else:
            data = tsv_to_list(data)
        col_numb = max([len(item) for item in data])
        for item in data:
            if len(item) != col_numb:
                raise MyException
        table = GoodTable(data)
    except FileNotFoundError:
        print('Файл не валиден')
    except (UnicodeError, SyntaxError, AttributeError, TypeError, IndexError):
        print('Формат не валиден')
