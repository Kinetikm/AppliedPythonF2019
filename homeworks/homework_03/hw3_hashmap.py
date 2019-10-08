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
            # TODO возвращаем ключ
            return self._key

        def get_value(self):
            # TODO возвращаем значение
            return self._value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self._key == other.get_key()

        def __iter__(self):
            yield self._key()
            yield self._value()

        # def __next__(self):
        #     return self.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.map = [[] for i in range(self.bucket_num)]
        self.capacity = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for entry in self.map[index]:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value

    def put(self, key, value):
        index = self._get_index(self._get_hash(key))
        new_put = self.Entry(key, value)
        if self.capacity >= 0.75*self.bucket_num:
            self._resize()
        for entry in self.map[index]:
            if entry.get_key() == key:
                self.map[index].remove(entry)
                self.map[index].append(new_put)
                return
        self.map[index].append(new_put)
        self.capacity += 1

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.capacity

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return (entry.get_value() for i in self.map for entry in i)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return (entry.get_key() for i in self.map for entry in i)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return ((entry.get_key(), entry.get_value()) for i in self.map for entry in i)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.bucket_num *= 2
        new_lst = self.items()
        self.capacity = 0
        self.map = [[] for i in range(self.bucket_num)]
        for entry in new_lst:
            self.put(*entry)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}".format(self.bucket_num, self.items())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)\
        return item in self.keys()
