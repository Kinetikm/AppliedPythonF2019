#!/usr/bin/env python
# coding: utf-8

# In[15]:


def check_palindrom(input_string):
    check_string = input_string[::-1]
    print(check_string)
    if input_string == check_string:
        return True
    else:
        return False


# In[ ]:
