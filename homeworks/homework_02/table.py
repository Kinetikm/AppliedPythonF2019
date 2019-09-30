import sys

# Ваши импорты
import print_table as prnt


if __name__ == '__main__':
    filename = sys.argv[1]

    # Ваш код
def table(file_name):
    prnt.prt_table(file_name)

if filename is not None:
    table(filename)
else:
    print("Файл не валиден")