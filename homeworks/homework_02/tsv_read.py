#!/usr/bin/env python
# coding: utf-8

import csv


def tsv_check(path_2_file, enc):
    with open(path_2_file, 'r', encoding=enc) as f:
        try:
            csv.reader(f, delimiter='\t')
            return True
        except:
            return False


def tsv_read(path_2_file, enc):
    result = []
    with open(path_2_file, 'r', encoding=enc) as f:
        reader = csv.reader(file, delimiter='\t')
        for i in reader:
            result.append(i)
    return result
