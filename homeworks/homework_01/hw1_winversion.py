#!/usr/bin/env python
# coding: utf-8

# In[78]:


def word_inversion(input_lst):
    input_lst.append(" ")
    input_lst.reverse()
    input_lst.append(" ")

    i = 1
    gap = 0

    while i < len(input_lst):
        if input_lst[i] == " ":
            word_len = i - gap - 1
            gap = i
            j = i - word_len
            k = 1
            while j < i - word_len + word_len / 2:
                temp = input_lst[j]
                input_lst[j] = input_lst[i - k]
                input_lst[i - k] = temp
                k = k + 1
                j = j + 1
        i = i + 1
    del input_lst[0]
    del input_lst[-1]
    # print(input_lst)
    return input_lst


# In[ ]:
