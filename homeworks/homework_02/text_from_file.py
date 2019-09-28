#!/usr/bin/env python
# coding: utf-8


import sys
import os


def get_text(filename):
    encodings = ['utf8', 'utf16', 'cp1251']
    text = ''
    for coding in encodings:
        try:
            with open(filename, "r", encoding=coding) as file:
                text = file.read().rstrip()
            return text
        except BaseException:
            continue
    return None
