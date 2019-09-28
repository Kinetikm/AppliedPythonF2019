import sys
from dummy_package import print_table as prt
# Ваши импорты

if __name__ == '__main__':
    filename = sys.argv[1]
    # Ваш код


def table(file_name):
    prt.prt_table(file_name)


if filename is not None:
    table(filename)
else:
    print("Файл не валиден")
