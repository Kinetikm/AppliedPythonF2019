#!/usr/bin/env python
# coding: utf-8


import copy


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
            self.key = key
            self.value = value

        def get_key(self):
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other):
            return self.get_key() == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.dict = [[] for i in range(bucket_num)]

    def get(self, key, default_value=None):
        ind = self._get_index(self._get_hash(key))
        for i in self.dict[ind]:
            if i.get_key() == key:
                return i.get_value()
        return default_value

    def put(self, key, value):
        if len(self.dict) == self.__len__():
            self._resize()
        ind = self._get_index(self._get_hash(key))
        for i in self.dict[ind]:
            if i.get_key() == key:
                i.value = value
                return
        self.dict[ind].append(HashMap.Entry(key, value))

    def __len__(self):
        return sum([len(i) for i in self.dict])

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % len(self.dict)

    def values(self):
        for i in self.dict:
            for j in i:
                yield j.get_value()

    def keys(self):
        for i in self.dict:
            for j in i:
                yield j.get_key()

    def items(self):
        for i in self.dict:
            for j in i:
                yield (j.get_key(), j.get_value())

    def _resize(self):
        new = copy.deepcopy(self.dict)
        self.dict = [[] for i in range(len(self.dict)*2)]
        for i in new:
            for j in i:
                self.put(j.get_key(), j.get_value())

    def __str__(self):
        return 'buckets: {}, items: {}'.format(len(self.dict), self.__len__())

    def __contains__(self, item):
        return self.get(item) is not None
