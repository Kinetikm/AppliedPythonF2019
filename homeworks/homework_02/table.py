#!/usr/bin/env python
# coding: utf-8


import sys
import os
from text_from_file import get_text
from struct_from_text import get_struct
from table_from_struct import get_table

if __name__ == '__main__':
    value = sys.argv[1]
    text_errs = ["Файл не валиден", "Формат не валиден", "Формат не валиден"]
    for i, func in enumerate([get_text, get_struct, get_table]):
        value = func(value)
        if value is None:
            value = text_errs[i]
            break
    print(value)
