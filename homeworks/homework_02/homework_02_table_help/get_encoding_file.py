import homeworks.homework_02.homework_02_table_help.encoding_list as encoding_list


def get_encoding_file(file_name):
    correct_encoding = ''
    for enc in encoding_list.encoding:
        with open(file_name, "r", encoding=enc) as file:
            try:
                file.read()
            except UnicodeError:
                pass
            else:
                correct_encoding = enc
                break
    return correct_encoding
