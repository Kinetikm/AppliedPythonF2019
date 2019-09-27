import sys

from terminaltables import AsciiTable
from tsv_read import tsv_read, is_tsv
from json_read import json_read, is_json
from detection import detection


class FormatError(Exception):
    print('Формат не валиден')
    sys.exit()


if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename, 'r')
        f.close()
    except FileNotFoundError:
        print('Файл не валиден')
    enc_type = detection(filename)
    if enc_type not in ['utf-8', 'utf-16', 'windows-1251']:
        raise FormatError
    elif not is_json(filename, enc_type):
        if not is_tsv(filename, enc_type):
            raise FormatError
        else:
            data = AsciiTable(tsv_read(filename, enc_type))
    else:
        data = AsciiTable(json_read(filename, enc_type))
    print(data.table)




