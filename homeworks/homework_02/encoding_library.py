#!/usr/bin/env python
# coding: utf-8


def find_encoding(file_name):
    encoding = ['utf8', 'utf16', 'cp1251']
    for e in encoding:
        try:
            open(file_name, encoding=e).read()
            open(file_name, encoding=e).close()
            return e
        except (UnicodeError, UnicodeDecodeError):
            continue
