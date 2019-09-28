import sys

# Ваши импорты
from read import read_file
from format_table import print_table
from encode import isvalid

if __name__ == '__main__':
    filename = sys.argv[1]

# Ваш код

try:
    correct_encoding = isvalid(filename)
    data = read_file(filename, correct_encoding)
    print_table(data)
except FileNotFoundError:
    print("Файл не валиден")
except (TypeError, UnicodeError, SyntaxError, AttributeError):
    print('Формат не валиден')
