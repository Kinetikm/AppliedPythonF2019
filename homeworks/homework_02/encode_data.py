#!/usr/bin/env python
# coding: utf-8


import sys


def encode_method(file_name):
    for encode in ("utf-16", "utf8", "cp1251"):
        try:
            with open(file_name, "r", encoding=encode) as f:
                f.readlines()
                f.close()
                return encode
        except FileNotFoundError:
            print("Файл не валиден")
            return None
        except (UnicodeDecodeError, UnicodeError):
            continue
    print("Формат не валиден")
    return None
