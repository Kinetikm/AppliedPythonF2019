import sys
from table_tsv import table_tsv
from table_json import table_json
# Ваши импорты


if __name__ == '__main__':
    filename = sys.argv[1]
    b = 'files\\'
    path = b + filename
    try:
        print(table_tsv(path))
    except FileNotFoundError , UnicodeError:
        print('Файл не валиден')
    except IndexError:
        try:
            print(table_json(name_of_fail))
        except JSONDecodeError:
            print('Формат не валиден')
    except:
        print('Формат не валиден')
