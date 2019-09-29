#!/usr/bin/env python
# coding: utf-8
 
 
def word_inversion(input_lst):
    input_lst.reverse()
    k = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            tmp = i
            for k in range(k, k + ((i - k + 1) // 2)):
                input_lst[k], input_lst[tmp-1] = input_lst[tmp-1], input_lst[k]
                tmp = tmp - 1
                k = k + 1
            k = i + 1
        if i == (len(input_lst)-1):
            tmp = i
            for j in range(k, k + ((i - k + 1) // 2)):
                input_lst[k], input_lst[tmp] = input_lst[tmp], input_lst[k]
                tmp = tmp - 1
                k = k + 1
    return input_lst
   
