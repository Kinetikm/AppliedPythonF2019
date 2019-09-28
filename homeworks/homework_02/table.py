import sys
<<<<<<< HEAD
import  table_printer
=======
import table_printer
>>>>>>> f0e30bc8dd8d4365ea17be6d250a4203029c6542
# Ваши импорты

if __name__ == '__main__':
    filename = sys.argv[1]


def table(file_name):
    table_printer.print_table(file_name)


if filename is not None:
    table(filename)
else:
    print("Файл не валиден")
