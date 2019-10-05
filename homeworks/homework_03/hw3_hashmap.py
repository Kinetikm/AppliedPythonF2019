#!/usr/bin/env python
# coding: utf-8


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
            self._key = key
            self._value = value

        def get_key(self):
            return self._key

        def get_value(self):
            return self._value

        def set_value(self, value):
            self._value = value

        def __eq__(self, other):
            return self._key == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._table = [[] for _ in range(bucket_num)]
        self._n = 0
        self._size = bucket_num
        self._RESIZING_FACTOR = 4
        self._FILLING_LIMIT = 2./3

    def get(self, key, default_value=None):
        """метод get, возвращающий значение, если оно присутствует, иначе default_value"""
        index = self._get_index(self._get_hash(key))
        for item in self._table[index]:
            if item.get_key() == key:
                return item.get_value()
        return default_value

    def put(self, key, value):
        index = self._get_index(self._get_hash(key))
        for item in self._table[index]:
            if item.get_key() == key:
                item.set_value(value)
                return
        self._table[index].append(self.Entry(key, value))
        self._n += 1
        if self._n > self._size * self._FILLING_LIMIT:
            self._resize()

    def __len__(self):
        return self._n

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self._size

    def values(self):
        for bucket in self._table:
            for entry in bucket:
                yield entry.get_value()

    def keys(self):
        for bucket in self._table:
            for entry in bucket:
                yield entry.get_key()

    def items(self):
        for bucket in self._table:
            for entry in bucket:
                yield entry.get_key(), entry.get_value()

    def _resize(self):
        tmp = HashMap(bucket_num=self._size*self._RESIZING_FACTOR)
        for key, value in self.items():
            tmp.put(key, value)
        self.__dict__.update(tmp.__dict__)

    def __str__(self):
        return 'buckets: {}, items: {}'.format(str(self._table),[(key, value) for key, value in self.items()])

    def __contains__(self, item):
        index = self._get_index(self._get_hash(item))
        for entry in self._table[index]:
            if entry.get_key() == item:
                return True
        return False
