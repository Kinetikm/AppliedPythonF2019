import sys
import file_read as f_read
import get_data
import table_print as t_print

if __name__ == '__main__':
    filename = sys.argv[1]
    encode = f_read.check_encode(path)
    if encode == "Формат не валиден" or encode == "Файл не валиден":
        print(encode)
    with open(filename, encoding=encode) as file:
        data_list = get_data.get_json_data_as_list(file)
    if data_list is None:
        with open(filename, encoding=encode) as file:
            data_list = get_data.get_tsv_data_as_list(file)
    t_print.print_data(data_list)
