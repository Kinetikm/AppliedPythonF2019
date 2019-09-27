#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv


def json_to_list(data):
    lst = []
    lst.append([key for key in data[0]])
    for dict_ in data:
        lst.append([dict_[key] for key in dict_])
    return lst


def csv_list_of_lists(path, enc):
    with open(file=path, mode='r', encoding=enc) as d:
        read = csv.reader(d, delimiter='\t')
        out = []
        for line in read:
            out.append(line)
    return out
