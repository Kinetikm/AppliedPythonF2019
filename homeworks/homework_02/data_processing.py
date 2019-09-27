#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def define_encoding(path):
    for enc in ['utf8', 'utf16', "cp1251"]:
        try:
            with open(file=path, mode='r', encoding=enc) as f:
                f.readline()
            return enc
        except UnicodeError:
            pass
        except FileNotFoundError:
            return "Файл не валиден"
        except SyntaxError:
            print('Формат не валиден')
        except AttributeError:
            print('Формат не валиден')
        except IndexError:
            print('Формат не валиден')
    return "Формат не валиден"


def column_size(data):
    sizes = [0]*len(data[0])
    for line in data:
        for i in range(len(data[0])):
            sizes[i] = max(sizes[i], len(str(line[i])))
    return sizes
