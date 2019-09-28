import sys

# Ваши импорты
from read import read_file
from format_table import print_table
from encode import isvalid


class MyError(Exception):
    pass

if __name__ == '__main__':
    filename = sys.argv[1]

# Ваш код


try:
    correct_encoding = isvalid(filename)
    data = read_file(filename, correct_encoding)
    len_ = len(data[0])
    for line in data:
        if len(line) != len_:
            raise MyError
except FileNotFoundError:
    print("Файл не валиден")
except (TypeError, UnicodeError, SyntaxError, AttributeError, IndexError, MyError):
    print('Формат не валиден')
else:
    print_table(data)
