#!/usr/bin/env python
# coding: utf-8

# In[14]:


#!/usr/bin/env python
# coding: utf-8

def reverse(number):
    minus=0
    if number<0:
        minus = True
    num_inv = 0
    str_num = str(abs(number))
    i = 0
    while i < len(str_num):
        num_inv = num_inv + int(str_num[-i-1]) * (10 ** (len(str_num)-i-1))
        i += 1
    if minus:
        num_inv = -num_inv
    return num_inv


# In[ ]:




