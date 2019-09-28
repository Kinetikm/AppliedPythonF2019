#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 22:41:34 2019

@author: altarion
"""


from collections import OrderedDict

from DataBase import DataBase
from DataBase import DataBaseError


class From_TSV_DataBase(DataBase):

    def __init__(self, data):
        self.keys = OrderedDict()
        for key in next(data):
            self.keys[key] = len(str(key))
        self.data = []
        for it in data:
            self.add_line(it)

    def add_line(self, line):
        if len(line) != len(self.keys):
            raise DataBaseError
        for i, key in enumerate(self.keys):
            self.keys[key] = max(self.keys[key], len(str(line[i])))
        self.data.append(line)
