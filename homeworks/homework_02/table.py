import sys

from terminaltables import AsciiTable
from define_encoding import define_enc
from type_json import json_tab, define_json
from type_tsv import tsv_tab, define_tsv

if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename, 'r')
        f.close()
    except FileNotFoundError:
        print("Файл не валиден")
    enc_type = define_enc(filename)
    if enc_type is None:
        print("Формат не валиден")
        sys.exit()
    if define_json(filename, enc_type):
        table = AsciiTable(json_tab(filename, enc_type))
    elif define_tsv(filename, enc_type):
        table = AsciiTable(tsv_tab(filename, enc_type))
    else:
        print("Формат не валиден")
        sys.exit()
    print(table.table)
