#!/usr/bin/env python
# coding: utf-8

import csv


def tsv_read(filename, enc):
    tdata = []
    with open(filename, 'r', encoding=enc) as file:
        reader = csv.reader(file, delimiter='\t')
        for i in reader:
            tdata.append(i)
    return tdata


def tsv_check(filename, enc):
        with open(filename, 'r', encoding=enc) as file:
            try:
                csv.reader(file, delimiter='\t')
                return 'tsv'
            except:
                return "Формат не валиден"
