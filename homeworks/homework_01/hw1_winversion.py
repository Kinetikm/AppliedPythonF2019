#!/usr/bin/env python
# coding: utf-8
 

def word_inversion(input_lst):
	try:
		input_lst.index(" ")
	except ValueError:
		return input_lst
	input_lst = input_lst[::-1]
	last = 0
	for i in range(len(input_lst) + 1):
		if (i == len(input_lst)) or (input_lst[i] == " "):
			if last == 0:
				input_lst[last:i] = input_lst[i-1::-1]
			else:
				input_lst[last:i] = input_lst[i-1:last-1:-1]
			last = i + 1
		return input_lst
