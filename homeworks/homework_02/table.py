import sys
from define_encoding import detect_encoding
from read_data import read_data
from create_table import build_table
# Ваши импорты


if __name__ == '__main__':
    filename = sys.argv[1]

    # Ваш код
    encoding = detect_encoding(filename)
    data = read_data(filename, encoding)
    table = build_table(data)
    print(table)
