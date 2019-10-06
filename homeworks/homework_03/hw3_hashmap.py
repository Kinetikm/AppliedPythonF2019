#!/usr/bin/env python
# coding: utf-8

import itertools


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
    class Entry:
        """
        Сущность, которая хранит пары ключ-значение
        :param key: ключ
        :param value: значение
        """
        def __init__(self, key, value):
            self.key = key
            self.value = value

        def get_key(self):
            # TODO возвращаем ключ
            return self.key

        def get_value(self):
            # TODO возвращаем значение
            return self.value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self.key == other

        def set_value(self, value):
            self.value = value

        def __str__(self):
            return "<" + self.key + ", " + self.value + ">"

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.buckets = [[] for i in range(bucket_num)]
        self.bucket_num = bucket_num
        self.capacity = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        if len(self.buckets[index]) != 0:
            for entry in self.buckets[index]:
                if entry.get_key() == key:
                    return entry.get_value()
        else:
            return default_value
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        if self.capacity >= self.bucket_num*(2/3):
            self._resize()
        index = self._get_index(self._get_hash(key))
        if len(self.buckets[index]) == 0:
            self.buckets[index].append(self.Entry(key, value))
            self.capacity += 1
        else:
            for entry in self.buckets[index]:
                if entry.get_key() == key:
                    if entry.get_value() != value:
                        entry.set_value(value)
                        return
                    else:
                        return
            self.buckets[index].append(self.Entry(key, value))
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
        it = 0
        for bucket in self.buckets:
            if it == 0:
                it = iter(entry.get_value() for entry in bucket)
            else:
                it = itertools.chain(it, iter(entry.get_value() for entry in bucket))
        return it

    def keys(self):
        # TODO Должен возвращать итератор ключей
        it = 0
        for bucket in self.buckets:
            if it == 0:
                it = iter(entry.get_key() for entry in bucket)
            else:
                it = itertools.chain(it, iter(entry.get_key() for entry in bucket))
        return it

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return zip(self.keys(), self.values())

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.bucket_num += 64
        new_buckets = [[] for i in range(self.bucket_num)]
        for bucket in self.buckets:
            if len(bucket) != 0:
                for entry in bucket:
                    index = hash(entry.get_key()) % self.bucket_num
                    new_buckets[index].append(entry)
        self.buckets = new_buckets

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        buckets = ",".join(str(bucket) for bucket in self.buckets)
        items = ",".join(str(item) for item in self.items())
        return "buckets: {" + buckets + "}, items:{" + items + "}"

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        for bucket in self.buckets:
            for entry in bucket:
                if entry == item:
                    return True
        return False
