#!/usr/bin/env python
# coding: utf-8


import sys
import json
import open_json
import open_tsv


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        open_json.open_json_file(filename)
    except json.decoder.JSONDecodeError:
        try:
            open_tsv.open_tsv_file(filename)
        except Warning:
            print("Формат не валиден")
    except FileNotFoundError:
        print("Файл не валиден")
