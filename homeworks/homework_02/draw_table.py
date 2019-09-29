#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def draw_table(text):
    max_len = {i: 0 for i in range(len(text[0].split("\t")))}
    lst = []
    for i in range(len(text)):
        lst.append(text[i].split("\t"))
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if len(lst[i][j]) > max_len[j]:
                max_len[j] = len(lst[i][j])
    sum_len = sum(list(max_len.values())) + 5 * len(max_len) + 1
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if i == 0:
                lst[i][j] = ("{:^" + str(max_len[j]) + "}").format(lst[i][j])
            elif j == len(lst[i]) - 1:
                lst[i][j] = ("{:>" + str(max_len[j]) + "}").format(lst[i][j])
            else:
                lst[i][j] = ("{:<" + str(max_len[j]) + "}").format(lst[i][j])
    table = "-" * sum_len + "\n"
    for line in lst:
        col = "|  {}  |\n".format("  |  ".join(line))
        table += col
    table += "-" * sum_len + "\n"
    print(table)
