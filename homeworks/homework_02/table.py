#!/usr/bin/env python
# coding: utf-8

import sys

from terminaltables import AsciiTable
from jsonreader import read as json_read, check as json_check
from tsvreader import read as tsv_read, check as tsv_check
import encodingdetector as enc_det


class FormatNotValidError(Exception):
    print('Формат не валиден')
    sys.exit()


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename, 'r')
        f.close()
    except OSError:
        print('Файл не валиден')
        sys.exit()
    encoding = enc_det(filename)
    if not encoding or not (json_check(filename) and json_read(filename)):
        raise FormatNotValidError
    elif json_check(filename):
        data = AsciiTable(json_read(filename, encoding))
    else:
        data = AsciiTable(tsv_read(filename, encoding))
    print(data.table)
