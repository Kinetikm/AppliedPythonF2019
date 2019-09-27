import sys

from json_read import json_read, json_check
from tsv_read import tsv_read, tsv_check
from encoding_define import encoding_define
from terminaltables import AsciiTable


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename, "r")
        f.close()
    except:
        print('Файл не валиден')
        sys.exit()
    enc = encoding_define(filename)
    if enc not in ['utf-8', 'utf-16', 'windows-1251']:
        print('Формат не валиден')
        sys.exit()
    if json_check(filename, enc):
        table = AsciiTable(json_read(filename, enc))
    elif tsv_check(filename, enc):
        table = AsciiTable(tsv_read(filename, enc))
    print(table.table)
