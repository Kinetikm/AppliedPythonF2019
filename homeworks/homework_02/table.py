import sys

from read_json import read_json, check_json
from read_tsv import read_tsv, check_tsv
from encoding_define import encoding_define
from terminaltables import AsciiTable


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename, "r")
        f.close()
    except:
        return 'Файл не валиден'
    enc = enc_define(filename)
    if enc not in ['utf-8', 'utf-16', 'windows-1251']:
        return 'Файл не валиден'
    if check_json(filename, enc):
        table = AsciiTable(read_json(filename, enc))
    elif check_tsc(filename, enc):
        table = AsciiTable(read_tsv(filename, enc))
    print table.table
