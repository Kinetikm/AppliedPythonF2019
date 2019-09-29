import sys
from enc import enc
from json_read import json_check, json_read
from tsv_read import tsv_check, tsv_read
from table_print import print_table

if __name__ == '__main__':
    filename = sys.argv[1]
    try:
        f = open(filename, "r")
        f.close()
    except:
        print('Файл не валиден')
        sys.exit()
    en = enc(filename)
    if en not in ('utf-8', 'utf-16', 'cp1251'):
        print("Формат не валиден")
        sys.exit()
    if json_check(filename, en):
        print_table(json_read(filename, en))
    else:
        if tsv_check(filename, en):
            print_table(tsv_read(filename, en))
