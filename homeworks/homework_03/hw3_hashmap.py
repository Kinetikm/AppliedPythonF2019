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
            self.data = (key, value)

        def get_key(self):
            # TODO возвращаем ключ
            return self.data[0]

        def get_value(self):
            # TODO возвращаем значение
            return self.data[1]

        def set_value(self, value):
            self.data = (self.data[0], value)

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self.data[0] == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.length = bucket_num
        self._len = 0
        self.data = [[] for _ in range(bucket_num)]

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for entry in self.data[index]:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        if self._len / self.length > 3 / 4:
            self._resize()
        index = self._get_index(self._get_hash(key))
        for entry in self.data[index]:
            if key == entry.get_key():
                entry.set_value(value)
                return
        self.data[index].append(HashMap.Entry(key, value))
        self._len += 1

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self._len

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.length

    def values(self):
        # TODO Должен возвращать итератор значений
        for lists in self.data:
            for entry in lists:
                yield entry.get_value()

    def keys(self):
        # TODO Должен возвращать итератор ключей
        for lists in self.data:
            for entry in lists:
                yield entry.get_key()

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        for lists in self.data:
            for entry in lists:
                yield (entry.get_key(), entry.get_value())

    def _resize(self):
        from copy import copy
        # TODO Время от времени нужно ресайзить нашу хешмапу
        _map = HashMap(self.length * 2)
        for key, value in self.items():
            _map.put(key, value)
        self._len = _map._len
        self.length = _map.length
        self.data = copy(_map.data)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f"buckets: {self.length}, items: {self._len}"

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        index = self._get_index(self._get_hash(item))
        for entry in self.data[index]:
            if entry.get_key() == item:
                return True
        return False
