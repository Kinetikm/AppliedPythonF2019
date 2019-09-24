#!/usr/bin/env python
# coding: utf-8


import sys
from other_methods import json2lists
from read_data import read_json_data, def_enc_method
from table_builder import table_builder

# Ваши импорты

if __name__ == '__main__':
    filename = sys.argv[1]

    # Ваш код
    checker = False
    try:
        data = read_json_data(filename, def_enc_method(filename))
        max_len = max([len(i) for i in data])
        for i in data:
            if len(i) != max_len:
                print('Формат не валиден')
                break

        checker = True
    except FileNotFoundError:
        print('Файл не валиден')
    except UnicodeError:
        print('Формат не валиден')
    except SyntaxError:
        print('Формат не валиден')
    except AttributeError:
        print('Формат не валиден')
    except IndexError:
        print('Формат не валиден')
    if checker:
        if data[1] == 1:
            table_builder(data[0])
        else:
            table_builder(json2lists(data[0]))
