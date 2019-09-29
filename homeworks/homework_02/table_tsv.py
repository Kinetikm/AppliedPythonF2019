import csv
import valid
from table_header import table_header
from writer_of_line import writer_of_line


def table_tsv(name_of_fail):
    with open(name_of_fail, "r", encoding=valid.validen(name_of_fail)) as read_file:
        data = csv.reader(read_file, delimiter='\t')
        tit = next(data)
        data_1 = []
        for line in data:
            data_1.append(line)
    table = ''
    data_2 = list(zip(*data_1))
    max_list = []
    for i in data_2:
        max_list.append(max(i, key=lambda x: len(x)))
    max_list_int = []
    for i in range(len(max_list)):
        max_list_int.append(len(max_list[i]))
    table += table_header(tit, max_list_int) + '\n'
    for line in data_1:
        table += writer_of_line(line, max_list_int, tit) + '\n'
    table += table.split('\n')[0]
    return table
