#!/usr/bin/env python
# coding: utf-8


import csv
import tsv_read


def tsv_func(filename, using_code):
    with open(filename, encoding=using_code) as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        list_of_rows = []
        column_num = 0
        for row in reader:
            if (len(row) != column_num and column_num != 0):  # different number of columns in a row => not tsv
                raise Warning
            column_num = len(row)
            list_of_rows += [row]
        tsv_read.tsv_to_table(list_of_rows)


def open_tsv_file(filename):
    try:
        tsv_func(filename, 'utf-8')
    except UnicodeDecodeError:
        try:
            tsv_func(filename, 'utf-16')
        except UnicodeDecodeError:
            tsv_func(filename, 'cp1251')
