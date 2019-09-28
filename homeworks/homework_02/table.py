import sys
import table_printer
# Ваши импорты

if __name__ == '__main__':
    filename = sys.argv[1]


def table(file_name):
    table_printer.print_table(file_name)


if filename is not None:
    table(filename)
else:
    print("Файл не валиден")
