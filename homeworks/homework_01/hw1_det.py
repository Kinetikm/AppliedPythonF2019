#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
	indices = list(range(len(list_of_lists)))
	total = 0
	if len(list_of_lists) != len(list_of_lists[0]) or len(list_of_lists) == 0:
		return None
	if len(list_of_lists) == 1:
		return list_of_lists[0][0]
	if len(list_of_lists) == 2 or len(list_of_lists[0]) == 2:
		return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0]
	for fc in indices:
		matrix = list_of_lists
		matrix = matrix[1:]
		height = len(matrix)
		for i in range(height):
			matrix[i] = matrix[i][0:fc] + matrix[i][fc+1:]
		sign = (-1) ** (fc % 2)
		sub_det = calculate_determinant(matrix)
		total += sign * list_of_lists[0][fc] * sub_det
	return total
