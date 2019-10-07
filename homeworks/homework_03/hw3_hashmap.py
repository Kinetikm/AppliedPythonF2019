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
            # raise NotImplementedError

        def get_value(self):
            # TODO возвращаем значение
            return self._value
            # raise NotImplementedError

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self._key == other.get_key()
            # raise NotImplementedError

        def __iter__(self):
            return self

        def __next__(self):
            return self.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.map = [[] for i in range(self.bucket_num)]
        self.capacity = 0
        # raise NotImplementedError

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for entry in self.map[index]:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value
        # raise NotImplementedError

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        index = self._get_index(self._get_hash(key))
        new_put = self.Entry(key, value)
        if self.capacity >= 0.75*self.bucket_num:
            self._resize()
        if new_put in self.map[index]:
            self.map[index].remove(new_put)
            self.map[index].append(new_put)
        else:
            self.map[index].append(new_put)
            self.capacity += 1

        # raise NotImplementedError

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.capacity
        # raise NotImplementedError

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)
        # raise NotImplementedError

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num
        # raise NotImplementedError

    def values(self):
        # TODO Должен возвращать итератор значений
        return (entry.get_value() for i in self.map for entry in i)
        # raise NotImplementedError

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return (entry.get_key() for i in self.map for entry in i)
        # raise NotImplementedError

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return ((entry.get_key(), entry.get_value) for i in self.map for entry in i)
        # raise NotImplementedError

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.bucket_num *= 2
        items = self.items()
        self.map = [[] for i in range(self.bucket_num)]
        for entry in items:
            self.put(*entry)

        #raise NotImplementedError

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}".format(self.bucket_num, self.items())
        # raise NotImplementedError

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)\
        return item in self.keys()
        # raise NotImplementedError
