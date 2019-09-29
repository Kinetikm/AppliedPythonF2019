import sys

from open_file import read_file
from print_table import print_table
from file_enc import file_enc


if __name__ == '__main__':
    filename = sys.argv[1]


try:
    correct_enc = file_enc(filename)
    data = read_file(filename, correct_enc)
    max_len = max([len(i) for i in data])
    for i in data:
        if len(i) != max_len:
            print('Формат не валиден')
            break
except (TypeError, UnicodeError, SyntaxError, AttributeError, IndexError, FileNotFoundError):
    print('Формат не валиден')
else:
    print_table(data)
