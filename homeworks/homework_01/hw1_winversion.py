#!/usr/bin/env python
# coding: utf-8
 

def word_inversion(input_lst):
	p = 0
	for i, n in enumerate(input_lst):
		if n == ' ':
			input_lst = input_lst[:p] + input_lst[p:i][::-1] + input_lst[i:]
			p = i+1
		if i == len(input_lst)-1:
			input_lst = input_lst[:p] + input_lst[p:][::-1]
	return input_lst[::-1]
