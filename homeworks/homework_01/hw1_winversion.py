#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    size = len(input_lst)
	for i in range(size // 2):
		temp = input_lst[i]
		input_lst[i] = input_lst[size - 1 - i]
		input_lst[size - 1 - i] = temp 
	return input_lst
    raise NotImplementedError
