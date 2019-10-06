#!/usr/bin/env python
# coding: utf-8


class HashMap:
    class Entry:
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
            return self.key == other.key

    def __init__(self, bucket_num=64):
        self.length = bucket_num
        self.bucket = [None for _ in range(self.length)]

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        hash_for_key = self._get_hash(key)
        index = self._get_index(hash_for_key)
        if self.bucket[index] is not None:
            for i in self.bucket[index]:
                if i.get_key() == key:
                    return i.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        hash_for_key = self._get_hash(key)
        index = self._get_index(hash_for_key)
        if self.bucket[index] is None:
            self.bucket[index] = [self.Entry(key, value)]
        elif self.Entry(key, value) in self.bucket[index]:
            for new_value in self.bucket[index]:
                if new_value.key == key:
                    new_value.value = value
        else:
            self.bucket[index].append(self.Entry(key, value))

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        k = 0
        for list_bucket in self.bucket:
            if list_bucket is not None:
                k += len(list_bucket)
        return k

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.length

    def values(self):
        # TODO Должен возвращать итератор значений
        return list(j.value for i in self.bucket if i is not None for j in i)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return list(j.key for i in self.bucket if i is not None for j in i)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return list((j.key, j.value) for i in self.bucket if i is not None
                    for j in i)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.bucket += [None] * (self.length // 2)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}".format(self.bucket, self.items())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
