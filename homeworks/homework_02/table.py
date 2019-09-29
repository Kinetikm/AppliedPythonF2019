import sys

from terminaltables import AsciiTable
from tsv_read import tsv_read, is_tsv
from json_read import json_read, is_json
import define_enc

if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename, 'r')
        # f.close()
    except FileNotFoundError:
        print("Файл не валиден")
    enc_type = define_enc.define(filename)
    if enc_type is None:
        print("Формат не валиден")
        sys.exit()
    if is_json(filename, enc_type):
        data = AsciiTable(json_read(filename, enc_type))
    elif is_tsv(filename, enc_type):
        data = AsciiTable(tsv_read(filename, enc_type))
    else:
        print("Формат не валиден")
        sys.exit()

    print(data.table)
