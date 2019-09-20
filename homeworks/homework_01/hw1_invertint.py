#!/usr/bin/env python
# coding: utf-8


def reverse(number):
	res = 0
	while number != 0:	
		a =	number % 10
		number = number // 10
		res = res * 10 + a
	return res
