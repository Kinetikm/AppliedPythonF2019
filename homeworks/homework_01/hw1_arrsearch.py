#!/usr/bin/env python
# coding: utf-8


def find_indices(input_list, target):
    sols_dict = dict()
    for i, val in enumerate(input_list):
        if val in sols_dict:
            return [sols_dict[val], i]
        else:
            if (target - val) not in sols_dict:
                sols_dict[target - val] = i
    return None
