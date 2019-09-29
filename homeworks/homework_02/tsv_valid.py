#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy


def is_tsv_valid(text):
    lst_of_lst = copy.deepcopy(text)
    for i in range(len(text)):
        lst_of_lst[i] = lst_of_lst[i].split("\t")
    max_len = max([len(i) for i in lst_of_lst])
    for i in lst_of_lst:
        if len(i) != max_len:
            return False
    return True
