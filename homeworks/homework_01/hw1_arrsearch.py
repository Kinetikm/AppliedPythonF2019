#!/usr/bin/env python
# coding: utf-8


def find_indices(input_list, n):
    if len(input_list) == 0:
        return None
    tmp_dict = {input_list[0]: 0}
    for i in range(1, len(input_list)):
        x = tmp_dict.get(n - input_list[i])
        if x is not None:
            return [x, i]
        tmp_dict[input_list[i]] = i
    return None
