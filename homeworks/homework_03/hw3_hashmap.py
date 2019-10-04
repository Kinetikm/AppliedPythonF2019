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

    # реализация итераторов по ключу, значению и ключ-значению
    class IterKey:
        def __init__(self, hash_table):
            self.pointer = 0
            self.hash_table = hash_table
            self.keys = self.hash_table.list_of_keys

        def __iter__(self):
            return self

        def __next__(self):
            if self.pointer < len(self.keys):
                key = self.keys[self.pointer]
                self.pointer += 1
                return key
            else:
                raise StopIteration

    class IterVal(IterKey):
        def __next__(self):
            if self.pointer < len(self.keys):
                value = self.hash_table.get(self.keys[self.pointer])
                self.pointer += 1
                return value
            else:
                raise StopIteration

    class IterItem(IterKey):
        def __next__(self):
            if self.pointer < len(self.keys):
                key, value = self.keys[self.pointer], self.hash_table.get(self.keys[self.pointer])
                self.pointer += 1
                return key, value
            else:
                raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.buckets = bucket_num
        self.hash_table = [[] for i in range(self.buckets)]
        self.list_of_keys = []
        self.count_of_Entry = 0
        self.INDICATE = 0.8
        self.RESIZER = 3

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for entry in self.hash_table[index]:
            if key == entry.get_key():
                return entry.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        index = self._get_index(self._get_hash(key))
        if self.hash_table[index]:
            for i in range(len(self.hash_table[index])):
                self.hash_table[index][i] = self.Entry(key, value)
                return None
        self.hash_table[index].append(self.Entry(key, value))
        self.list_of_keys.append(key)
        self.count_of_Entry += 1
        if self.count_of_Entry > (self.INDICATE * self.buckets):
            self._resize()
        return None

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.count_of_Entry

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.buckets

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.IterVal(self)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.IterKey(self)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.IterItem(self)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        items = [self.get(key) for key in self.list_of_keys]
        self.buckets *= self.RESIZER
        remain = self.count_of_Entry
        del self.hash_table
        self.hash_table = [[] for i in range(self.buckets)]
        for key, value in zip(self.list_of_keys, items):
            self.put(key, value)
        self.count_of_Entry = remain

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}".format(self.buckets, self.count_of_Entry)

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return items in self.keys()
