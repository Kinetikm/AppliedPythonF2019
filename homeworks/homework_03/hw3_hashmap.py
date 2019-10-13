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
            self.key = key
            self.value = value

        def get_key(self):
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other):
            return self.key == other.key

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.length = bucket_num
        self._bucket = [None for _ in range(self.length)]
        self.capacity = 0
        self.threshold = 0.75

    def get(self, key, default_value=None):
        index = self._get_index(self._get_hash(key))
        if self._bucket[index] is not None:
            for var in self._bucket[index]:
                if var.get_key() == key:
                    return var.get_value()
        return default_value

    def put(self, key, value):
        if key not in self.keys():
            index = self._get_index(self._get_hash(key))
            if self._bucket[index] is None:
                self._bucket[index] = [self.Entry(key, value)]
            else:
                self._bucket[index].append(self.Entry(key, value))
            self.capacity += 1
        else:
            index = self._get_index(self._get_hash(key))
            if self._bucket[index]:
                for var in self._bucket[index]:
                    if var.key == key:
                        var.value = value
        if self.capacity / self.length > self.threshold:
            self._resize()

    def __len__(self):
        return self.capacity

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.length

    def values(self):
        res = []
        for item in self.items():
            res.append(item[1])
        return res

    def keys(self):
        res = []
        for item in self.items():
            res.append(item[1])
        return res

    def items(self):
        res = []
        for el in self._bucket:
            if el:
                for s in el:
                    res.append((s.get_key(), s.get_value()))
        return res

    def _resize(self):
        self._bucket.extend([None for _ in range(self.length)])
        self.length *= 2

    def __str__(self):
        return f"buckets: {self._bucket}, items: {self.items()}"

    def __contains__(self, item):
        return item in self.keys()
