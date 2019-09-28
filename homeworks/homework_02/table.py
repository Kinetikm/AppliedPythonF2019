import sys
import homeworks.homework_02.homework_02_table_help.get_encoding_file as get_encoding_file
import homeworks.homework_02.homework_02_table_help.get_json_tsv_data as get_data_helper
import homeworks.homework_02.homework_02_table_help.printer_as_table as printer_table


def show_table(filename):
    try:
        encode = get_encoding_file.get_encoding_file(filename)
        with open(filename, encoding=encode) as file:
            list_data = get_data_helper.get_json_data_as_list(file)
        if list_data is None:
            with open(filename, encoding=encode) as file:
                list_data = get_data_helper.get_tsv_data_as_list(file)
        printer_table.print_data_as_table(list_data)
        if list_data is None:
            print("Формат не валиден")
    except FileNotFoundError:
        print("Файл не валиден")


if __name__ == '__main__':
    filename = sys.argv[1]
    show_table(filename)
    # Ваш код
