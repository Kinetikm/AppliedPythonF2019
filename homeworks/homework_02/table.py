#!/usr/bin/env python
# coding: utf-8
import sys
import json
import csv
from dropinf import out_table
from Transfer import json_transfer, tsv_transfer
from MyEncode import give_encode


def main(filename):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print("Файл не валиден")
        return False

    code = give_encode(filename)
    if not code:
        print("Формат не валиден")
        return False

    try:
        file = open(filename, "r", encoding=code)
        data = json.load(file)
        format = "json"
    except json.decoder.JSONDecodeError:
        try:
            file = open(filename, "r", encoding=code)
            data = list(csv.reader(file))
            format = "tsv"
        except Exception:
            print("Формат не валиден")
            return False

    if format == "tsv":
        data = tsv_transfer(data)
    elif format == "json":
        data = json_transfer(data)
    else:
        print("Формат не валиден")
        return False

    if not data:
        print("Формат не валиден")
        return False
    out_table(data)
    file.close()


if __name__ == '__main__':
    filename = sys.argv[1]
main(filename)
