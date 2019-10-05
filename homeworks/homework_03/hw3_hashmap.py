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
            #  возвращаем ключ
            return self.key

        def get_value(self):
            #  возвращаем значение
            self.value

        def __eq__(self, other):
            #  реализовать функцию сравнения
            self.key == other.key

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.container = [[] for t in range(bucket_num)]
        self.bucket_num = bucket_num
        self.filled = 0

    def get(self, key, default_value=None):
        #  метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for t in self.container[index]:
            if t.get_key() == key:
                default_value = t.get_value()
        return default_value

    def put(self, key, value):
        #  метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        item = self.Entry(key, value)
        index = self._get_index(self._get_hash(key))
        if self.container[index] is not None:
            for i in self.container[index]:
                if i.get_key() == key:
                    i = item
                    return

        self.container[index].append(item)
        self.filled += 1
        if self.__len__() / self.bucket_num > 0.67:
            self._resize()

    def __len__(self):
        #  Возвращает количество Entry в массиве
        return self.filled

    def _get_hash(self, key):
        #  Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        #  По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        #  Должен возвращать итератор значений
        return (item.get_value() for array in self.container for item in array)

    def keys(self):
        #  Должен возвращать итератор ключей
        return (item.get_key() for array in self.container for item in array)

    def items(self):
        #  Должен возвращать итератор пар ключ и значение (tuples)
        return ((item.get_key(), item.get_value) for array in self.container for item in array)

    def _resize(self):
        #  Время от времени нужно ресайзить нашу хешмапу
        self.filled = 0
        tmp = self.container.copy()
        self.bucket_num *= 2
        self.container = [[] for t in range(self.bucket_num)]
        for array in tmp:
            for i in range(len(array)):
                self.put(array[i].get_key(), array[i].get_value())

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, self.__len__())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        index = self._get_index(self._get_hash(item))
        for i in range(len(self.container[index])):
            return self.container[i].get_key() == item
