#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    if len(input_lst) > 0:
        dc = dict()
        dc2 = dict()
        if num == input_lst[0]:
            return(0, 0)
        else:
            dc[input_lst[0]] = 0
        for i in range(1, len(input_lst)):
            if num == input_lst[i]:
                return(i, i)
            # проверяем, есть ли подходящая последовательность
            elif (dc.get(num - input_lst[i]) is not None):
                return (dc.get(num - input_lst[i]), i)
            else:
                # формируем все возможные последовательности
                for j in list(dc.keys()):
                    dc2[j + input_lst[i]] = dc[j]
                # удаляем ненужные пары, не дающие последовательность
                # со следующими элементами
                dc = dc2
                dc2 = dict()
                dc[input_lst[i]] = i
    return ()
