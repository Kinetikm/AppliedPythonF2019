import sys
# import utils
from gtable import GoodTable
from methods import json_to_list, tsv_to_list
from reading import read_file


if __name__ == '__main__':
    # Ваш код
    filename = sys.argv[1]
    try:
        data, flag_json = read_file(filename)
        if flag_json:
            data = json_to_list(data)
        else:
            data = tsv_to_list(data)
        table = GoodTable(data)
        table.print_table()
    except FileNotFoundError:
        print('Файл не валиден')
    except TypeError:
        print('Формат не валиден')
