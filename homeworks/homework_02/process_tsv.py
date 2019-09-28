import csv


class FormatError(Exception):
    def __init__(self, text):
        self.txt = text


def check_format(lst_of_lst):
    cols_num = len(lst_of_lst[0])
    for lst in lst_of_lst:
        if len(lst) != cols_num:
            raise FormatError("Формат не валиден")


def process_tsv(filename, encoding):
    try:
        file_ = open(filename, 'r', encoding=encoding)
        data = csv.reader(file_, delimiter="\t")
        full_text = []
        for line in data:
            full_text.append(line)
        file_.close()
        check_format(full_text)
        return full_text
    except OSError:
        print('Файл не валиден')
    finally:
        file_.close()
