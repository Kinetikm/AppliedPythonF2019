#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 22:38:46 2019

@author: altarion
"""


from collections import OrderedDict

from DataBase import DataBase
from DataBase import DataBaseError


class From_JSON_DataBase(DataBase):

    def __init__(self, data):
        self.keys = OrderedDict()
        self.data = []
        for line in data:
            self.add_line(line)

    def add_line(self, line):
        if type(line) != dict:
            raise DataBaseError
        for it, value in line.items():
            self.keys[it] = max(self.keys.get(it, 0), len(str(value)))
        self.data.append(tuple(line.values()))

    def print_base(self):
        for it in self.keys:
            self.keys[it] = max(self.keys[it], len(it))
        super().print_base()
