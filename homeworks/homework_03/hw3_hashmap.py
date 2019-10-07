#!/usr/bin/env python
# coding: utf-8


class HashMap:
    class Entry:
        def __init__(self, key, value):
            """
            Сущность, которая хранит пары ключ-значение
            :param key: ключ
            :param value: значение
            """
            self.__key = key
            self.__val = value

        def get_key(self):
            return self.__key

        def get_value(self):
            return self.__val

        def __eq__(self, other):
            return self.__key == other.get_key()

        def __iter__(self):
            yield self.__key
            yield self.__val

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bnum = bucket_num
        self.hmap = list(list() for i in range(self.bnum))
        self.__len = 0

    def get(self, key, default_value=None):
        # метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        i = self._get_index(self._get_hash(key))
        for entry in self.hmap[i]:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        i = self._get_index(self._get_hash(key))
        put_entry = self.Entry(key, value)
        for idx, entry in enumerate(self.hmap[i]):
            if entry == put_entry:
                self.hmap[i].pop(idx)
                self.__len -= 1
                break
        self.hmap[i].append(put_entry)
        self.__len += 1
        llen = 0
        for lst in self.hmap:
            if lst:
                llen += 1
        if llen > self.bnum * 0.70710678:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.__len

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bnum

    def values(self):
        # TODO Должен возвращать итератор значений
        return [entry.get_value() for entry in self.items()]

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return [entry.get_key() for entry in self.items()]

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        ret = list()
        for hlst in self.hmap:
            for entry in hlst:
                ret.append(entry)
        return ret

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.bnum *= 2
        items = self.items()
        self.hmap = list(list() for i in range(self.bnum))
        self.__len = 0
        for entry in items:
            self.put(entry.get_key(), entry.get_value())

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: '+str(self.bnum)+', items: '+str(len(self))

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        if item in self.keys():
            return True
        return False
