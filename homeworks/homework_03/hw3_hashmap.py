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

        def __eq__(self, other):
            return self._value == other.get_key()

        def __iter__(self):
            yield self._key
            yield self._value

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._table = [[] for _ in range(bucket_num)]
        self._n = 0
        self._keys = []
        self._size = bucket_num
        self._RESIZING_RANGE = 4
        self._FILLING_LIMIT = 2./3

    def get(self, key, default_value=None):
        for item in self._table[self._get_index(self._get_hash(key))]:
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
        self._keys.append(key)
        if self._n > self._FILLING_LIMIT * self._size:
            self.resize()

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
        tmp_items = [[key, value] for key, value in self.items()]
        self._table = [[] for _ in range(self._size * self._RESIZING_RANGE)]
        for item in tmp_items:
            self.put(item[0], item[1])

    def __str__(self):
        return 'buckets: {}, items: {}'.format(str(self._table), [(key, self.get(key)) for key in self._keys])

    def __contains__(self, item):
        return item in self._keys

    def get_keys(self):
        return self._keys
