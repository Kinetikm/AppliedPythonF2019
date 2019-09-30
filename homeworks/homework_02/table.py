import sys

# Ваши импорты
from test_data_reader import json_reading, tsv_reading
from help_file import to_know_encoding
from beautiful_output import create_field


if __name__ == '__main__':
    filename = sys.argv[1]

    # Ваш код
    en = to_know_encoding(filename)
    try:
        with open(filename, 'r', encoding=en) as f:
            info = json_reading(f)
        if info is None:
            with open(filename, 'r', encoding=en) as f:
                info = tsv_reading(f)
        if info is None:
            print('Формат не валиден')
        num_col = len(info[0])
        create_field(info, num_col)
    except IOError:
        print("Файл не валиден")
