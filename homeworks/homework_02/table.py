import sys
import table_printer


if __name__ == '__main__':
    filename = sys.argv[1]


if filename is not None:
    table_printer.table_print(filename)
else:
    print("Файл не валиден")
