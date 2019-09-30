#!/usr/bin/env python
# coding: utf-8


def to_know_encoding(filename):
    with open(filename, 'rb') as f:
        info = f.read()
        try:
            info.decode("UTF-8")
            return "UTF-8"
        except UnicodeDecodeError:
            return "cp1251"
