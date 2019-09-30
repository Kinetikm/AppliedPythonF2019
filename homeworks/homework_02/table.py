#!/usr/bin/env python
# coding: utf-8

import sys
from file_writer import File_Writer
from place_in_table import place_in_table

if __name__ == '__main__':
    filename = sys.argv[1]
    data = File_Writer(filename)
    if data is None:
        exit()
    else:
        table = place_in_table(data)
        if table is None:
            exit()
        else:
            print(table)
