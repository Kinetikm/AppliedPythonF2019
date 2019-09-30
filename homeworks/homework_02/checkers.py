import json
import csv
import sys


def encoding_check(file):
    for enc in ['utf-16', 'utf8', 'cp1251']:
        try:
            with open(file, encoding=enc) as file_c:
                file_c.readlines()
                file_c.close()
            return enc
        except UnicodeError:
            continue
    return False


def is_file_valid():
    try:
        open(sys.argv)
        return sys.argv
    except FileNotFoundError:
        return False


def is_json(file, enc):
    with open(file, encoding=enc) as file_c:
        try:
            list_of_key = []
            checker = json.load(file_c)
            list_of_key.append(list(checker[0].keys()))
            for key in checker:
                if list(key.keys()) != list_of_key[0] or list(key.keys()) == []:
                    return False
                list_of_key.append(list(key.values()))
            return True
        except (json.JSONDecodeError, KeyError, IndexError):
            return False


def is_tsv(file, enc):
    with open(file, encoding=enc) as file_c:
        data = csv.reader(file_c, delimiter='\t')
        for key in data:
            if len(key) == 0:
                return False
        return True


def is_int(x):
    try:
        x = int(x)
        return True
    finally:
        return False
