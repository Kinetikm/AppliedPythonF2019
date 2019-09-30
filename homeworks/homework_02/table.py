#!/usr/bin/env python
# coding: utf-8

import sys
import json
from encoding_library import find_encoding
from conversion_library import conversion_to_columns, strings_tsv, strings_json
from table_library import frame_print

if __name__ == '__main__':
    filename = sys.argv[1]

    try:
        strings_json(filename)
        z = []
        n = strings_json(filename)[0]
        for k in strings_json(filename):
            if len(k) == len(n):
                z.append(0)
            else:
                z.append(1)

        if sum(z) != 0:
            print('Формат не валиден')
        else:
            frame_print(strings_json(filename), conversion_to_columns(strings_json(filename)))

    except json.JSONDecodeError:
        strings_tsv(filename)
        z = []
        n = strings_tsv(filename)[0]
        for k in strings_tsv(filename):
            if len(k) == len(n):
                z.append(0)
            else:
                z.append(1)

        if sum(z) != 0:
            print('Формат не валиден')
        else:
            frame_print(strings_tsv(filename), conversion_to_columns(strings_tsv(filename)))

    except FileNotFoundError:
        print('Файл не валиден')
