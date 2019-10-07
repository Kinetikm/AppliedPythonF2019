#!/usr/bin/env python
# coding: utf-8


class HashMap:
    class Entry:
        def __init__(self, key, value):
            self.key = key
            self.value = value

        def get_key(self):
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self.key == other.key

    def __init__(self, bucket_num=64):
        self.amount = bucket_num
        self.buckets = [None] * self.amount

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        hash_of_key = self._get_hash(key)
        index = self._get_index(hash_of_key)
        if self.buckets[index] is None:
            return default_value
        else:
            for value in self.buckets[index]:
                if value.get_key() == key:
                    return value.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        index = self._get_index(self._get_hash(key))
        if self.buckets[index] is None:
            self.buckets[index] = [self.Entry(key, value)]
        elif self.Entry(key, value) in self.buckets[index]:
            for item in self.buckets[index]:
                if item.key == key:
                    item.value = value
        else:
            self.buckets[index].append(self.Entry(key, value))

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return len(self.items())

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.amount

    def values(self):
        # TODO Должен возвращать итератор значений
        return list(item.value for bucket in self.buckets if bucket is not None for item in bucket)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return list(item.key for bucket in self.buckets if bucket is not None for item in bucket)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return list((item.key, item.value) for bucket in self.buckets if bucket is not None for item in bucket)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        buckets_tmp = self.buckets[::]
        self.amount = self.amount * 2
        self.buckets = [[] for _ in range(self.amount)]
        for bucket in buckets_tmp:
            for item in range(len(bucket)):
                self.put(bucket[item].get_key(), bucket[item].get_value())

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}".format(self.buckets, len(self))

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
