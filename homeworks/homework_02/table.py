import sys

from read_data import *
from print_table import *
from format import *

if __name__ == '__main__':
    filename = sys.argv[1]

    try:
        data = read_data_from_file(filename)
        data = format_change(data)
        pretty_print_table(data)
    except FileNotFoundError:
        print("Файл не валиден")
    except UnicodeDecodeError:
        print("Формат не валиден")
    except:
        print("Формат не валиден")
