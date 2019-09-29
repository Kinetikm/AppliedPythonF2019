import json
import valid
from table_header import table_header
from writer_of_line import writer_of_line


def table_json(name_of_fail):
    with open(name_of_fail, "r", encoding=valid.validen(name_of_fail)) as read_file:
        data = json.load(read_file)
    name_of_raw = []
    for i in data:
        for key in i:
            if key not in name_of_raw:
                name_of_raw.append(key)
    data_2 = []
    for i in range(len(data[0])):
        data_2.append([])
    for i in data:
        for j in range(len(i)):
            data_2[j].append(str(i.get(name_of_raw[j])))
    max_list = []
    for i in data_2:
        max_list.append(max(i, key=lambda x: len(x)))
    max_list_int = []
    for i in range(len(max_list)):
        max_list_int.append(len(max_list[i]))
    table = ''
    table += table_header(name_of_raw, max_list_int) + '\n'
    for i in data:
        line_ = []
        for j in i:
            line_.append(str(i.get(j)))
        table += writer_of_line(line_, max_list_int, name_of_raw) + '\n'
    table += table.split('\n')[0]
    return table
