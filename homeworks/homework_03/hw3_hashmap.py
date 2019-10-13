#!/usr/bin/env python
# coding: utf-8
from itertools import chain


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
    class Entry:
        def __init__(self, key, value):
            """
            Сущность, которая хранит пары ключ-значение
            :param key: ключ
            :param value: значение
            """
            self.__key = key
            self.__value = value

        def get_key(self):
            return self.__key

        def get_value(self):
            return self.__value

        def __eq__(self, other):
            return True if self.__key == other.get_key() else False

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.__table = [[] for _ in range(bucket_num)]
        self.__bucket_num = bucket_num
        self.__items = 0

    def get(self, key, default_value=None):
        index = self._get_index(self._get_hash(key))
        for item in self.__table[index]:
            if item.get_key() == key:
                return item.get_value()
        return default_value

    def put(self, key, value):
        if self.__items / self.__bucket_num > 1.5:
            self._resize()
        index = self._get_index(self._get_hash(key))
        item = HashMap.Entry(key, value)
        for i, el in enumerate(self.__table[index]):
            if el.get_key() == key:
                self.__table[index][i] = item
                return
        self.__table[index].append(item)
        self.__items += 1

    def __len__(self):
        return self.__items

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.__bucket_num

    def values(self):
        return (item.get_value() for item in chain(*(ch for ch in self.__table)))

    def keys(self):
        return (item.get_key() for item in chain(*(ch for ch in self.__table)))

    def items(self):
        return ((item.get_key(), item.get_value()) for item in chain(*(ch for ch in self.__table)))

    def _resize(self):
        new_bucket_num = self.__bucket_num * 2
        new_table = [[] for _ in range(new_bucket_num)]
        for item in chain(*(ch for ch in self.__table)):
            index = hash(item.get_key()) % new_bucket_num
            new_table[index].append(item)
        self.__bucket_num = new_bucket_num
        self.__table = new_table

    def __str__(self):
        print(f"buckets: {self.__bucket_num}, items: {self.__items}")

    def __contains__(self, item):
        index = self._get_index(self._get_hash(item))
        for element in self.__table[index]:
            if element.get_key() == item:
                return True
        return False
