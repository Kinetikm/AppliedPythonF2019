#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 19:11:34 2019

@author: altarion
"""


from collections import OrderedDict


class DataBaseError(IndexError):
    pass


class DataBase:
    """Хранится в опертивной памяти"""

    def __init__(self):
        """
            В self.keys хранятся названия стобцов,
            в self.data сами данные
            Конструктор не должен вызываться у этого класса,
            только у потомков, реализовавших методы
            __init__ и add_line
        """
        self.keys = OrderedDict()
        self.data = []

    def add_line(self, line):
        """Добавляет новую строку в базу данных"""

    def check_valid_format(self):
        """
            Обходит весь массив и проверяет на несовпадение
            количества ключей и длины строк
            Если где-то несовпало, значит файл не валиден
        """
        valid = True
        for it in self.data:
            if len(it) != len(self.keys):
                valid = False
                break
        if not valid:
            raise DataBaseError

    def print_base(self):
        """Печатает отфарматированную базу данных"""
        self.check_valid_format()
        length = 4 * len(self.keys) + sum(self.keys.values()) + len(self.keys) + 1
        horizontal_line = ""
        for _ in range(length):
            horizontal_line += '-'
        print(horizontal_line)

        head_str = "|"
        for key, value in self.keys.items():
            head_str += "  " + str(key).center(value) + "  |"
        print(head_str)

        keys = list(self.keys.keys())
        res = keys[len(keys) - 1]
        keys = keys[0:len(keys) - 1]

        for i in range(len(self.data)):
            title = "|"
            for j, key in enumerate(keys):
                title += "  " + str(self.data[i][j]).ljust(self.keys[key]) + "  |"
            title += "  " + str(self.data[i][-1]).rjust(self.keys[res]) + "  |"
            print(title)
        print(horizontal_line)
