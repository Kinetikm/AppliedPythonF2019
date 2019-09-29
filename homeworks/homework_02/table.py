#!/usr/bin/env python
# coding: utf-8


import sys
from terminaltables import AsciiTable
from encode import encoding
from check import checking
from read import reading


if __name__ == '__main__':
    filename = sys.argv[1]

    enc = encoding(file_name)
    check = checking(file_name, enc)
    read = reading(file_name, enc, check)
    table = AsciiTable(read)
    print(table.table)
