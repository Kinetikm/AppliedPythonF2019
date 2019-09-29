#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import csv


class DataBaseError(IndexError):
    pass


def mb_json(f):
    try:
        a = json.load(f)
    except json.decoder.JSONDecodeError:
        a = None
    return a


def mb_tsv(f):
    try:
        a = csv.reader(f, delimiter='\t')
    except csv.Error:
        a = None
    return a


def try_print(parse_func, a):
    try:
        base = parse_func(a)
        base.print_base()
    except DataBaseError:
        print("Формат не валиден")


def check_encoding_(path, encoding=["utf8", "utf16", "cp1251"]):
    for encod in encoding:
        try:
            f = open(f"{path}", encoding=encod)
            f.read()
        except UnicodeError:
            pass
        else:
            return encod, False
        finally:
            f.close()
    return None, True


def check_encoding(path, encoding={"utf-8", "utf-16", "windows-1251"}):
    import chardet
    with open(f"{path}", "rb") as f:
        _data = f.read()
        _format = chardet.detect(_data)["encoding"]

    if _format not in encoding:
        print("Формат не валиден")
        return None, True
    return _format, False
