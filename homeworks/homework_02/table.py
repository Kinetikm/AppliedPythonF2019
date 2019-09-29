import sys
from homeworks.homework_02.filereader import file_read
from homeworks.homework_02.data_table import DataTable
from homeworks.homework_02.tsv_json_reading import file_to_data

if __name__ == '__main__':
    filename = sys.argv[1]
    table = DataTable()
    err_code, file = file_read(filename)
    if err_code == 1:
        print("Файл не валиден")
    elif err_code == 2:
        print('Формат не валиден')
    else:
        err_code, header, rows = file_to_data(file)
        if err_code == 1:
            print("Формат не валиден")
        else:
            table.header_to_datatable(header)
            for row in rows:
                table.row_to_datatable(row)
            table.table_output()
