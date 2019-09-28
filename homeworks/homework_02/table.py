import sys

from table_make import make_table
from raw_read import raw_text
from format_read import read_format
# Ваши импорты

if __name__ == '__main__':
    filename = sys.argv[1]
    txt = raw_text(filename)
    if not txt:
        print('Файл не валиден')
    else:
        txt = read_format(txt)
        if not txt:
            print('Формат не валиден')
        else:
            print(make_table(txt))
