#!/usr/bin/env python
# coding: utf-8

# In[26]:


import sys
import data_processing
from format_to_list import json_to_list, csv_list_of_lists
from table_build import table_builder


if __name__ == '__main__':
    filename = sys.argv[1]
    table_builder(filename)




