import sys
from os import path
from check_data import encoding_check
from data_read import read_data
from make_table import do_table

if __name__ == '__main__':
    filename = sys.argv[1]
if not path.exists(filename):
    print("Файл не валиден")
else:
    text_mas = ["Файл не валиден", "Формат не валиден", "Формат не валиден2"]
    result = filename
    for i, func in enumerate([encoding_check, read_data, do_table]):
        result = func(result)
        if result is None:
            result = text_mas[i]
            break
    print(result)
