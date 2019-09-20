#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    n = 0
	size = len(input_lst)
	lst = [0 for i in range(size)]
	while n < size:
		for i in range(size - n):
			lst[i] += input_lst[i+n]
			if lst[i] == num:
				return (i, i + n)
		n += 1		
	return ()
