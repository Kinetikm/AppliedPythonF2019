import sys

from terminaltables import AsciiTable
from tsv_read import tsv_read, is_tsv
from json_read import json_read, is_json
from detection import detection_enc


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename, 'r')
        f.close()
    except FileNotFoundError:
        print('Файл не валиден')
    enc_type = detection_enc(filename)
    if enc_type is None:
        sys.exit()
    elif not is_json(filename, enc_type):
        if not is_tsv(filename, enc_type):
            print('Формат не валиден')
            sys.exit()
        else:
            data = AsciiTable(tsv_read(filename, enc_type))
    else:
        data = AsciiTable(json_read(filename, enc_type))
    print(data.table)
