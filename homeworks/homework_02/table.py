import sys
import printer

if __name__ == '__main__':
    filename = sys.argv[1]


def result(file_name):
    printer.print_t(file_name)


if filename is not None:
    result(filename)
else:
    print("Файл не валиден")
