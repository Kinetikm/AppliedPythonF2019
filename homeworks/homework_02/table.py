import sys
from file_reading import reading
from formated_table import format_table, print_table


if __name__ == '__main__':
    filename = sys.argv[1]
    a = reading(filename)
    if a is not None:
        print_table(format_table(a))
