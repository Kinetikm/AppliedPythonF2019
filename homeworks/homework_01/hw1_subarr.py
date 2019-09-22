#!/usr/bin/env python
# coding: utf-8

# In[26]:


def find_subarr(input_lst, num):
    lst = input_lst
    dict = {}
    no_sum = True
    sum = 0
    i = 0
    while i < len(lst):
        j = i
        while j < len(lst):
            if i == j:
                sum += lst[i]
            else:
                sum += lst[j]
            dict[sum] = i, j
            if sum == num:
                no_sum = False
                return dict[sum]
            j += 1
        sum = 0
        i += 1
    if no_sum:
        return tuple()


# In[ ]:
