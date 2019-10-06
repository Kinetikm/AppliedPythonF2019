#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """

    class Iterator:
        def __init__(self, table, name=None):
            self._table = table
            self._name = name
            self._cur1 = 0
            self._cur2 = 0

        def __iter__(self):
            return self

        def __next__(self):
            while self._cur1 < len(self._table):
                if self._cur2 < len(self._table[self._cur1]):
                    element = self._table[self._cur1][self._cur2]
                    if self._name == "keys":
                        element = element.get_key()
                    elif self._name == "values":
                        element = element.get_value()
                    else:
                        element = (element.get_key(), element.get_value())
                    self._cur2 += 1
                    return element
                self._cur1 += 1
                self._cur2 = 0
            raise StopIteration

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
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other):
            return self.key == other.get_key()

    def __init__(self, _buckets_num=64):
        """
        Реализуем метод цепочек
        :param _buckets_num: число бакетов при инициализации
        """
        self._buckets_num = _buckets_num
        self._table = [[] for _ in range(self._buckets_num)]
        self._entries_num = 0
        self._buckets_usd = 0

    def get(self, key, default_value=None):
        index = self._get_index(self._get_hash(key))
        for i, element in enumerate(self._table[index]):
            if element.get_key() == key:
                return element.get_value()
        else:
            return default_value

    def put(self, key, value):

        item = self.Entry(key, value)
        index = self._get_index(self._get_hash(key))
        if not self.__contains__(key):
            self._entries_num += 1
            if len(self._table[index]) == 0:
                self._buckets_usd += 1
            self._table[index].append(item)
        else:
            for i, element in enumerate(self._table[index]):
                if element.get_key() == item.get_key():
                    self._table[index][i] = item
        if self._buckets_usd / self.__len__() < 3 / 2:
            self._resize()

    def __len__(self):
        return self._entries_num

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self._buckets_num

    def values(self):
        return self.Iterator(self._table, "values")

    def keys(self):
        return self.Iterator(self._table, "keys")

    def items(self):
        return self.Iterator(self._table)

    def _resize(self):
        self._entries_num = 0
        array = []
        self._buckets_num *= 4
        for item in self.items():
            array.append(item)
        self._table = []
        for i in range(self._buckets_num):
            self._table.append([])
        for i, element in enumerate(array):
            item = self.Entry(element[0], element[1])
            self.put(item.get_key(), item.get_value())

    def __str__(self):
        return "buckets: {}, items: {}".format(self._buckets_num, self.__len__())

    def __contains__(self, item):
        index = self._get_index(self._get_hash(item))
        for i, element in enumerate(self._table[index]):
            if element.get_key() == item:
                return True
