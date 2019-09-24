#!/usr/bin/env python
# coding: utf-8


from json import load, dumps, decoder
import csv


def def_enc_method(path):
    for el in ['utf8', 'utf16', 'cp1251']:
        try:
            with open(file=path, mode='r', encoding=el) as file:
                file.readline()
            return el
        except UnicodeError:
            continue


def read_tsv_data(path, encoding_method):
    global tsv_type
    tsv_type = True
    with open(file=path, mode='r', encoding=encoding_method) as file:
        data = csv.reader(file, delimiter="\t")
        output = []
        for line in data:
            output.append(line)
        return output


def read_json_data(path, encoding_method):
    try:
        with open(file=path, mode='r', encoding=encoding_method) as file:
            data = load(file)
            return (data, 0)
    except decoder.JSONDecodeError:
        return (read_tsv_data(path, encoding_method), 1)
