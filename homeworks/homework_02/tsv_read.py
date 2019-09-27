#!/usr/bin/env python
# coding: utf-8

import csv


def tsv_check(path_2_file, enc):
    with open(path_2_file, 'r', encoding=enc) as f:
        try:
            csv.reader(f)
            return True
        except:
            return False


def tsv_read(path_2_file, enc):
    result = []
    with open(path_2_file, 'r', encoding=enc) as f:
        reader = csv.reader(f, delimiter='\t')
        for i in reader:
            print(i)
            result.append(i)
    return result
