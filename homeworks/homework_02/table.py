import sys

# Ваши импорты
import open_file
import read_format
import create_table


if __name__ == '__main__':
    filename = sys.argv[1]
    error, text = open_file.open(filename)
    if error == 1:
        print("Файл не валиден")
    elif error == 2:
        print("Формат не валиден")
    else:
        (error, title, rows) = read_format.read(text)
        if error == 1:
            print("Формат не валиден")
        else:
            create_table.print_table(title, rows)
