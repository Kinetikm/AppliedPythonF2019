#!/usr/bin/env python
# coding: utf-8

# In[51]:


def calculate_determinant(list_of_lists):
    matrix = list_of_lists
    is_matrix = True
    det = 0

    i = 0
    while i < len(matrix):
        if len(matrix) != len(matrix[i]):
            is_matrix = False
            return None
        i += 1
    if is_matrix:
        if len(matrix) > 2:
            i = 0
            k = 1
            while i < len(matrix):
                minor = list()
                j = 0
                while j < (len(matrix) - 1):
                    minor.append(matrix[j + 1][::])
                    j += 1
                j = 0
                while j < (len(matrix) - 1):
                    del(minor[j][i])
                    j += 1
                det += matrix[0][i] * k * calculate_determinant(minor)
                k = k * (-1)
                i += 1
            return det

        if len(matrix) == 2:
            det = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
            return det

        if len(matrix) == 1:
            det = matrix[0]
            if isinstance(det, list):
                det = matrix[0][0]
            return det


# In[ ]:
