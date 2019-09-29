import sys
import print_table

if __name__ == '__main__':
    filename = sys.argv[1]

if filename is not None:
    print_table.table_print(filename)
else:
    print("Файл не валиден")
