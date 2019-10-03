import csv
import json
import type_x
from tabulate import tabulate


def open_tcv(file_name):
    with open(file_name) as fd:
        table = []
        rd = csv.reader(fd, delimiter="\t", quotechar="")
        for row in rd:
            table.append(row)
            print(tabulate(table, headers=["Название", "Теги", "Ссылка", "Оценка"], stralign='center'))


def open_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
        keys = data.keys()
        print(tabulate(keys, tablefmt='orgtbl', stralign='center'))
        for index, row in enumerate(data[keys[0]]):
            print(tabulate(data[keys[0]][index], data[keys[1]][index],
                           data[keys[2]][index], tablefmt='orgtbl', stralign='center'))


def ch_print(file_name):
    try:
        value = type_x(file_name)
        if value:
            return open_json(value)
        value = type_x(file_name)
        if value:
            return open_tcv(value)
    except FileNotFoundError:
        print("Файл не валиден")
    except UnicodeDecodeError:
        print("Формат не валиден")
