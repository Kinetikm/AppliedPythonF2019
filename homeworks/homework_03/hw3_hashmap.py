#!/usr/bin/env python
# coding: utf-8
from itertools import chain


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
            return True if self.__key == other.get_key() else False

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.__table = [[] for _ in range(bucket_num)]
        self.__bucket_num = bucket_num
        self.__items = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for item in self.__table[index]:
            if item.get_key() == key:
                return item.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        if self.__items / self.__bucket_num > 1.5:
            self._resize()
        index = self._get_index(self._get_hash(key))
        item = HashMap.Entry(key, value)
        for i, el in enumerate(self.__table[index]):
            if el.get_key() == key:
                self.__table[index][i] = item
                return
        self.__table[index].append(item)
        self.__items += 1

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.__items

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.__bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return (item.get_value() for item in chain(*(ch for ch in self.__table)))

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return (item.get_key() for item in chain(*(ch for ch in self.__table)))

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return ((item.get_key(), item.get_value()) for item in chain(*(ch for ch in self.__table)))

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        new_bucket_num = self.__bucket_num + 32
        new_table = [[] for _ in range(new_bucket_num)]
        for item in chain(*(ch for ch in self.__table)):
            print(item)
            index = hash(item.get_key()) % new_bucket_num
            new_table[index].append(item)
        self.__bucket_num = new_bucket_num
        del self.__table
        self.__table = new_table

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        print(f"buckets: {self.__bucket_num}, items: {self.__items}")

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        for element in self.keys():
            if element == item:
                return True
        return False
