#!/usr/bin/env python
# coding: utf-8
import random
import time

import numpy as np
import itertools


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """

    class Iter:
        def __init__(self, hashmap):
            self.map = []
            for el in hashmap:
                if el:
                    for pair in el:
                        self.map.append(pair)

    class IterKeys(Iter):
        def __init__(self, hashmap):
            super().__init__(hashmap)
            self.pos = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.pos == len(self.map):
                raise StopIteration
            key = self.map[self.pos].get_key()
            self.pos += 1
            return key

    class IterValues(Iter):
        def __init__(self, hashmap):
            super().__init__(hashmap)
            self.pos = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.pos == len(self.map):
                raise StopIteration
            value = self.map[self.pos].get_value()
            self.pos += 1
            return value

    class IterItems(Iter):
        def __init__(self, hashmap):
            super().__init__(hashmap)
            self.pos = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.pos == len(self.map):
                raise StopIteration
            key, value = self.map[self.pos].get_key(), self.map[self.pos].get_value()
            self.pos += 1
            return key, value

    class Entry:
        def __init__(self, key, value):
            """
            Сущность, которая хранит пары ключ-значение
            :param key: ключ
            :param value: значение
            """
            self.key = key
            self.value = value

        def get_key(self):
            # TODO возвращаем ключ
            return self.key

        def get_value(self):
            # TODO возвращаем значение
            return self.value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self.key == other

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.size = 0
        self.coefficient = 2
        self.bucket_num = bucket_num
        self.map = [None for _ in range(self.bucket_num)]

    def get(self, key, default_value=None):
        key_hash = self._get_hash(key)
        key_index = self._get_index(key_hash)
        if self.map[key_index]:
            for i in self.map[key_index]:
                if key == i:
                    return i.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        key_hash = self._get_hash(key)
        key_index = self._get_index(key_hash)
        if self.map[key_index] is None:
            self.map[key_index] = [self.Entry(key, value)]
            self.size += 1
            return True
        for i in self.map[key_index]:
            if i == key:
                i.value = value
                return True
        self.size += 1
        self.map[key_index].append(self.Entry(key, value))
        return True

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.size

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        values = []
        for elem in self.map:
            if elem:
                for pair in elem:
                    values.append(pair.get_value())
        return self.IterValues(self.map)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.IterKeys(self.map)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.IterItems(self.map)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.map += [None for _ in range((self.coefficient - 1) * self.bucket_num)]
        self.bucket_num *= self.coefficient
        return True

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}".format(self.bucket_num, self.size)

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        key_hash = self._get_hash(item)
        key_index = self._get_index(key_hash)
        if self.map[key_index]:
            for i in self.map[key_index]:
                if item == i:
                    return True
        return False
