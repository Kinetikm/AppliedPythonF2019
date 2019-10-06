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
            self.__key = key
            self.__value = value

        def get_key(self):
            return self.__key

        def get_value(self):
            return self.__value

        def __eq__(self, other):
            return self.__key == other.get_key()

        def __iter__(self):
            yield self.__key
            yield self.__value

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.h_map = [[] for i in range(int(self.bucket_num))]
        self.check = 0.75

    def get(self, key, default_value=None):
        h_id = self._get_index(self._get_hash(key))
        for ent in self.h_map[h_id]:
            if ent.get_key() == key:
                return ent.get_value()
        return default_value

    def put(self, key, value):
        h_id = self._get_index(self._get_hash(key))
        item = self.Entry(key, value)
        for i, ent in enumerate(self.h_map[h_id]):
            if ent == item:
                self.h_map[h_id].pop(i)
                break
        self.h_map[h_id].append(item)
        counter = self.bucket_num * self.check

        if len([lst for lst in self.h_map if lst]) > counter:
            self._resize()

    def __len__(self):
        return len(self.items())

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.bucket_num

    def values(self):
        return [ent.get_value() for ent in self.items()]

    def keys(self):
        return [ent.get_key() for ent in self.items()]

    def items(self):
        return [ent for lst_of_ent in self.h_map for ent in lst_of_ent]

    def _resize(self):
        self.bucket_num *= 2
        items = self.items()
        self.h_map = [[] for i in range(self.bucket_num)]
        for ent in items:
            self.put(ent.get_key(), ent.get_value())

    def __str__(self):
        return 'buckets: {}, items: {}'.format(self.bucket_num, len(self))

    def __contains__(self, item):
        return item in self.keys()
