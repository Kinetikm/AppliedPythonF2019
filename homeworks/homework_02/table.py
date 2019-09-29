import sys

# Ваши импорты
from homeworks.homework_02.table_view import Table
from homeworks.homework_02.file_reader import read_file
from homeworks.homework_02.json_tsv_reader import extract_data

if __name__ == '__main__':
    filename = sys.argv[1]
    table = Table()
    ret_code, data = read_file(filename)
    if ret_code == 1:
        print("Файл не валиден")
    elif ret_code == 2:
        print("Формат не валиден")
    else:
        (ret_code, header, rows) = extract_data(data)
        if ret_code == 1:
            print("Формат не валиден")
        else:
            table.add_header(header)
            for row in rows:
                table.add_row(row)
            table.print_table()
