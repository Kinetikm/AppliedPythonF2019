#!/usr/bin/env python
# coding: utf-8

import sys
import json
from for_table import import_data, processing, table_creator


def opening(filename):
    encoding = ["utf8", "cp1251", "utf16", "ASCII"]
    json_status = False
    for enc in encoding:
        try:
            with open(filename, "r", encoding=enc) as f:
                data = json.load(f)
                json_status = True
                break
        except json.decoder.JSONDecodeError:
            with open(filename, "r", encoding=enc) as f:
                data = f.read()
                json_status = False
                break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            return "file_not_found", False
    else:
        raise UnicodeDecodeError("Неизвестная кодировка")
    return data, json_status


def data_to_json(data):
    lines = data.split("\n")
    output_list = []
    a = {}
    if lines[0] != "":
        keys = lines[0].split("\t")
    length = len(keys)
    for i in range(1, len(lines) - 1):
        line = lines[i]
        line_list = line.split("\t")
        if len(line_list) != length or line_list[0] == "":
            return False
        a = {keys[0]: line_list[0],
             keys[1]: line_list[1],
             keys[2]: line_list[2],
             keys[3]: line_list[3]
             }
        output_list.append(a)
    return output_list, keys


def check_data(data, keys=[], json_status=False):
    if not json_status:
        if data == "file_not_found":
            print("Файл не валиден")
            return False
        elif not data:
            print("Формат не валиден")
            return False
        else:
            return True
    else:
        for var in data:
            if list(var.keys()) != keys:
                print("Формат не валиден")
                return False
    return True


def max_values(data):
    max_name, max_link, max_tag, max_mark = (0, 0, 0, 0)
    for var in data:
        if len(var["Название"]) > max_name:
            max_name = len(var["Название"])
        if len(var["Ссылка"]) > max_link:
            max_link = len(var["Ссылка"])
        if len(var["Теги"]) > max_tag:
            max_tag = len(var["Теги"])
    return max_name, max_link, max_tag


def line_creator(func):
    def wrapper(data, keys):
        head_str = ""
        max_name, max_link, max_tag, table_len, table_data = func(data, keys)
        head_name = (max_name + 4 - len("Название")) // 2
        head_link = (max_link + 4 - len("Ссылка")) // 2
        head_tag = (max_tag + 4 - len("Теги")) // 2
        head_mark = 2
        if table_len != 0:
            head_str += "|" + " " * head_name + keys[0] + " " * head_name + \
                        "|" + " " * head_link + keys[1] + " " * head_link + \
                        "|" + " " * head_tag + keys[2] + " " * head_tag + \
                        "|" + " " * head_mark + keys[3] + " " * head_mark + "|"
        else:
            head_str += f"|  {keys[0]}  |  {keys[1]}  "
            head_str += f"|  {keys[2]}  |  {keys[3]}  |"
            table_len = len(head_str)
        return "-" * table_len + "\n" + head_str + \
               "\n" + table_data + "-" * table_len

    return wrapper


@line_creator
def creator(data, keys):
    table = ""
    table_len = 0
    max_name, max_link, max_tag = max_values(data)
    mark_len = len(keys[3]) + 1
    first = True
    for var in data:
        name = var[keys[0]]
        link = var[keys[1]]
        tags = var[keys[2]]
        mark = var[keys[3]]
        table += f"|  {name}" + " " * (2 + max_name - len(name))
        table += f"|  {link}" + " " * (2 + max_link - len(link))
        table += f"|  {tags}" + " " * (2 + max_tag - len(tags))
        table += "|" + " " * mark_len + f"{mark}" + "  |"
        if first:
            table_len = len(table)
            first = False
        table += "\n"
    return max_name, max_link, max_tag, table_len, table


if __name__ == '__main__':
    filename = sys.argv[1]

    data, json_status = import_data.opening(filename)
    if json_status:
        keys = list(data[0].keys())
    if not processing.check_data(data, json_status=False):
        sys.exit()
    if not json_status:
        data, keys = processing.data_to_json(data)
        json_status = True
        if data is False:
            print("Формат не валиден")
            sys.exit()
    if processing.check_data(data, keys=keys, json_status=True):
        output = table_creator.creator(data, keys)
        print(output)
    else:
        sys.exit()
