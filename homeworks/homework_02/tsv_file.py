# -*- coding: utf-8 -*-

import csv


def tsv_data(tsv_file, cod):
    list_dicts = []
    file = open(tsv_file, encoding=cod)
    tsv = csv.DictReader(file, delimiter="\t")
    for line in tsv:
        list_dicts.append(dict(line))
    return list_dicts
