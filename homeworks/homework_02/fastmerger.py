#!/usr/bin/env python
# coding: utf-8

from .heap import MaxHeap
import copy


class FastSortedListMerger:

    @staticmethod
    def merge_first_k(list_of_lists, k):
        """
        принимает на вход список отсортированных непоубыванию списков и число
        на выходе выдает один список длинной k, отсортированных по убыванию
        """
        output_list = []
        full_list = []
        new_list = copy.deepcopy(list_of_lists)
        for i, var in enumerate(new_list):
            if isinstance(var, list) and var != []:
                element = (var.pop(), i)
                full_list.append(element)
            elif isinstance(var, int):
                element = (new_list.pop(i), -1)
                full_list.append(element)
        h = MaxHeap(full_list)
        while len(output_list) != k and h.heap:
            maximum, idx = h.extract_maximum()
            output_list.append(maximum)
            if idx != -1 and new_list[idx]:
                element = (new_list[idx].pop(), idx)
                h.add(element)
        return output_list
