#!/usr/bin/env python
# coding: utf-8

# In[8]:


def check_palindrom(input_string):
    i = 0
    while i < len(input_string) / 2:
        if input_string[i] == input_string[-i - 1]:
            return True
        else:
            return False
        i += 1


# In[ ]:
