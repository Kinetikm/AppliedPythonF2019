#!/usr/bin/env python
# coding: utf-8


from numpy import *
x = range(16)
x = reshape(x,(4,4))
print(range(x.shape[0]))
print(x[ix_([0,2,3],[1,3])])
