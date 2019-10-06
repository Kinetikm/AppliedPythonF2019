#!/usr/bin/env python
# coding: utf-8


class HashMap:
    class Entry:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            """
            Сущность, которая хранит пары ключ-значение
            :param key: ключ
            :param value: значение
            """

        def get_key(self):
            return self.key
            # TODO возвращаем ключ

        def get_value(self):
            return self.value
            # TODO возвращаем значение

        def __eq__(self, other):
            return self.get_key() == other.get_key()
            # TODO реализовать функцию сравнения

    def __init__(self, bucket_num=67):
        self.size = bucket_num
        self.list = [[] for s in range(self.size)]

    def get(self, key, default_value=None):
        index = self._get_index(self._get_hash(key))
        for s in self.list[index]:
            if s.get_key() == key:
                return s.get_value()
        return default_value

    def put(self, key, value):
        index = self._get_index(self._get_hash(key))
        while len(self.list) < self.size:
            self.list.append([])
        new = self.Entry(key, value)
        if new in self.list[index]:
            self.list[index].remove(new)
        self.list[index].append(new)
        if len([1 for s in self.list if s]) > self.size * 0.5:
            self._resize

    def __len__(self):
        return len(self.items())

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.size

    def values(self):
        return ([s.get_value() for case in self.list for s in case])

    def keys(self):
        return ([s.get_key() for case in self.list for s in case])

    def items(self):
        return ([(s.get_key(), s.get_value()) for case in self.list for s in case])

    def __str__(self):
        return ("buckets: {}, items: {}".
                format(self.size, len(self.items())))

    def __contains__(self, item):
        return item in self.keys()
