#!/usr/bin/env python
# coding: utf-8

import sys
from print_table import *
from json_csv_read import *
from read_file import *

if __name__ == '__main__':
    filename = sys.argv[1]

    try:
        data = read_utf8(filename)
        if data is None:
            data = read_utf16(filename)
        if data is None:
            data = read_cp1251(filename)
        data = read_json(data)
        if not data:
            data = read_csv(data)
        if data[0] == 'json':
            json = data[1]
            k = json[0].keys()
            text = ['\t'.join(k)]
            for i in json:
                line = []
                for j in k:
                    line.append(str(j[i]))
                text.append('\t'.join(line))
        if data[0] == 'csv':
            text = data[1]
        print_table(text)
    except UnicodeDecodeError:
        print('Формат не валиден')
        sys.exit(1)
    except FileNotFoundError:
        print("Файл не валиден")
        sys.exit(1)
    except:
        print("Файл не валиден")
