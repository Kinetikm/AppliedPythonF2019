import sys


from func_read import read_data
from func_print import print_inf
from functions import json_or_csv, open_file, find_enc


if __name__ == '__main__':
    filename = sys.argv[1]

try:
    open_file(filename)
    type_f = find_enc(filename)
    encoding = json_or_csv(filename, type_f)
    print_inf(read_data(filename, type_f, encoding))
except FileNotFoundError:
    print("Файл не валиден")
except UnicodeDecodeError:
    print("Формат не валиден")
except AssertionError:
    print("Формат не валиден")
