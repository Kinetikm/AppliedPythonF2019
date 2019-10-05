#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """

    class Entry:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            """
            Сущность, которая хранит пары ключ-значение
            :param key: ключ
            :param value: значение
            """

        def get_key(self):
            return self.key
            # TODO возвращаем ключ

        def get_value(self):
            return self.value
            # TODO возвращаем значение

        def __eq__(self, other):
            return self.key == other.key
            # TODO реализовать функцию сравнения

    def key_generator(self):
        for bucket in self.H:
            if bucket is not None:
                for elem in bucket:
                    yield elem.key

    def value_generator(self):
        for bucket in self.H:
            if bucket is not None:
                for elem in bucket:
                    yield elem.value

    def item_generator(self):
        for bucket in self.H:
            if bucket is not None:
                for elem in bucket:
                    yield elem.key, elem.value

    def __init__(self, bucket_num=64):
        self._length = 0
        self.H = [None] * bucket_num
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """

    def get(self, key, default_value=None):
        hash_val = self._get_hash(key)
        index = self._get_index(hash_val)
        if self.H[index] is None:
            return default_value
        i = 0
        while i != len(self.H[index]) - 1 and key != self.H[index][i].key:
            i += 1
        if key != self.H[index][i].key:
            return default_value
        return self.H[index][i].value
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value

    def put(self, key, value):
        if len(self.H) < self.__len__() + 1:
            self._resize()
        if not self.__contains__(key):
            self._length += 1
        hash_val = self._get_hash(key)
        index = self._get_index(hash_val)
        if self.H[index] is None:
            self.H[index] = [HashMap.Entry(key, value)]
        else:
            self.H[index].insert(0, HashMap.Entry(key, value))
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self._length

    def _get_hash(self, key):
        return hash(key)
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет

    def _get_index(self, hash_value):
        return hash_value % len(self.H)
        # TODO По значению хеша вернуть индекс элемента в массиве

    def values(self):
        return self.value_generator()
        # TODO Должен возвращать итератор значений

    def keys(self):
        return self.key_generator()
        # TODO Должен возвращать итератор ключей

    def items(self):
        return self.item_generator()
        # TODO Должен возвращать итератор пар ключ и значение (tuples)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.H.extend([None] * self._length)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f'buckets: {{{len(self.H)}}}, items: {{{self.__len__()}}}'

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        if item in self.keys():
            return True
        return False
