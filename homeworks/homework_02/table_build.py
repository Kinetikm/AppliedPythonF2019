#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
from data_processing import define_encoding, column_size
from format_to_list import json_to_list, csv_list_of_lists


def table_builder(path):
    enc = define_encoding(path)
    if enc == "Формат не валиден" or enc == "Файл не валиден":
        print(enc)
        return enc
    with open(file=path, mode="r", encoding=enc) as f:
        try:
            data = json_to_list(json.load(f))
        except Exception:
            data = csv_list_of_lists(path, enc)
    column_count = max(len(line) for line in data)
    for line in data:
        if len(line) != column_count:
            return "Формат не валиден"
    sizes = column_size(data)
    dash = "-" * (sum(sizes) + 4 * len(sizes) + 5)
    print(dash)
    for i, line in enumerate(data):
        if i == 0:
            for j in range(len(data[0])):
                print("|", end="")
                print('{0:^{1}}'.format(line[j], sizes[j] + 4), end="")
            print("|", end="")
            print("\n", end="")
        else:
            for j in range(len(data[0])):
                if j == len(data[0]) - 1:
                    print("|", end="")
                    print('{0:>{1}}'.format(line[j], sizes[j] + 2), end="  |")
                else:
                    print("|  ", end="")
                    print('{0:<{1}}'.format(line[j], sizes[j]), end="  ")
            if j != len(data[0]) - 1:
                print("\n")
            else:
                print("\n", end="")
    print(dash)