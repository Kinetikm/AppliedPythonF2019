import sys
from readers import read_json, read_tsv
from encoding_selector import detect_encoding
from table_printer import print_table


def main(filename):
    encoding = detect_encoding(filename)
    try:
        with open(filename, 'r', encoding=encoding) as file:
            data = read_json(file)
        if data is None:
            with open(filename, 'r', encoding=encoding) as file:
                data = read_tsv(file)
        if data is None:
            print('Формат не валиден')
            return
        num_columns = len(data[0])
        print_table(data, num_columns)

    except IOError:
        print("Файл не валиден")


if __name__ == '__main__':
    input_param = sys.argv[1]
    main(input_param)
