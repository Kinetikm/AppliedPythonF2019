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
            return self.key == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.size = 1/3
        self.resize = 2
        self.hash_table = [[] for _ in range(self.bucket_num)]

    def get(self, key, default_value=None):
        index = self._get_index(self._get_hash(key))
        if self.__contains__(key):
            for element in self.hash_table[index]:
                if element.get_key() == key:
                    return element.get_value()
        return default_value

    def put(self, key, value):
        index = self._get_index(self._get_hash(key))
        key_exit = False
        bucket = self.Entry(key, value)
        for i, kv in enumerate(self.hash_table[index]):
            if bucket == kv:
                key_exit = True
                break
        if key_exit:
            self.hash_table[index].pop(i)
            self.hash_table[index].append(bucket)
        else:
            self.hash_table[index].append(bucket)
        j = 0
        for buckets in self.hash_table:
            if buckets:
                j += 1
        if j > self.bucket_num*self.size:
            self._resize()

    def __len__(self):
        return len(self.items())

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.bucket_num

    def values(self):
        return [kv.get_value() for bucket in self.hash_table for kv in bucket]

    def keys(self):
        return [kv.get_key() for bucket in self.hash_table for kv in bucket]

    def items(self):
        result_lst = []
        for bucket in self.hash_table:
            for kv in bucket:
                result_lst.append((kv.get_key(), kv.get_value()))
        return result_lst

    def _resize(self):
        self.bucket_num *= self.resize
        buckets = self.items()
        self.hash_table = [[] for _ in range(self.bucket_num)]
        for kv in buckets:
            key, value = kv
            self.put(key, value)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, len(self))

    def __contains__(self, item):
        index = self._get_index(self._get_hash(item))
        for element in self.hash_table[index]:
            if element.get_key() == item:
                return True
