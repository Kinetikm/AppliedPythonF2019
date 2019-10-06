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
            # TODO возвращаем ключ
            return self.key

        def get_value(self):
            # TODO возвращаем значение
            return self.value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self.key == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.ar = [[] for i in range(bucket_num)]
        self.buckets = bucket_num
        self.elements = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        bucket = self._get_index(self._get_hash(key))
        for i in self.ar[bucket]:
            if i.get_key() == key:
                return i.get_value()
        else:
            return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        i = self._get_index(self._get_hash(key))
        new_elem = self.Entry(key, value)
        for elem in self.ar[i]:
            if elem.get_key() == new_elem.get_key():
                elem.value = value
                return
        self.ar[i].append(new_elem)
        self.elements += 1
        # if self.elements > self.buckets * 2 / 3:
        #     self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.elements

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.buckets

    def values(self):
        # TODO Должен возвращать итератор значений
        iterator = []
        for buc in self.ar:
            iterator.extend([elem.get_value() for elem in buc])
        return iter(iterator)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        iterator = []
        for buc in self.ar:
            iterator.extend([elem.get_key() for elem in buc])
        return iter(iterator)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        iterator = []
        for buc in self.ar:
            iterator.extend([(elem.get_key(), elem.get_value()) for elem in buc])
        return iter(iterator)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.buckets *= 2
        new = [[] for i in range(self.buckets)]
        for buc in self.ar:
            for elem in buc:
                i = self._get_index(self._get_hash(elem.key))
                new[i].append(elem)
        self.ar = new

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f"buckets: {self.ar}, items: {self.items()}"

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        for buc in self.ar:
            for elem in buc:
                if elem.get_key() == item:
                    return True
        return False
