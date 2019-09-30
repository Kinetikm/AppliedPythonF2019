#!/usr/bin/env python
# coding: utf-8


import sys


def encod(file_name):
    for en in ("utf8", "utf-16", "cp1251"):
        try:
            with open(file_name, "r", encoding=en) as f:
                f.readlines()
                f.close()
                return en
        except FileNotFoundError:
            print("Файл не валиден")
            return None
        except (UnicodeDecodeError, UnicodeError):
            continue
    print("Формат не валиден")
    return None
