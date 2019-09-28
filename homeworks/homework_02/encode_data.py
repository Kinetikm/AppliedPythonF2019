#!/usr/bin/env python
# coding: utf-8


import sys


def ch_encod(file_name):
    for en in ("utf-16", "utf8", "cp1251"):
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