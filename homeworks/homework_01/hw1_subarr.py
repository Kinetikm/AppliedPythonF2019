#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    tmp = {}
    sum = 0
    for indx, zn in enumerate(input_lst):
        sum += zn
<<<<<<< HEAD
        if sum - num in tmp:
            return(tmp[sum - num], indx)
        elif zn == num:
            return(indx, indx)
        else:
            tmp[sum - zn] = indx
=======
        if sum - num in dict:
            return(dict[sum - num], indx)
        elif zn == num:
            return(indx, indx)
        else:
            dict[sum - val] = indx
>>>>>>> c20400d4c8e92a8680a05d4ddfc00d72e104f789
    return()
