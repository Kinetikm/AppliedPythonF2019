#!/usr/bin/env python
# coding: utf-8


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
            head_str += "|" + " "*head_name + keys[0] + " "*head_name + \
                        "|" + " "*head_link + keys[1] + " "*head_link + \
                        "|" + " "*head_tag + keys[2] + " "*head_tag + \
                        "|" + " "*head_mark + keys[3] + " "*head_mark + "|"
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
