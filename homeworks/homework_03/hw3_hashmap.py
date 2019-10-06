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
        self.size = bucket_num
        self.buckets = [None] * self.size

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        key_hash = self._get_hash(key)
        key_index = self._get_index(key_hash)

        if self.buckets[key_index] is not None:
            for i in self.buckets[key_index]:
                if i.get_key() == key:
                    return i.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        key_hash = self._get_hash(key)
        key_index = self._get_index(key_hash)

        if self.__len__() > 2 * self.size // 3:
            self._resize()

        if self.buckets[key_index] is None:
            self.buckets[key_index] = [self.Entry(key, value)]
        elif self.Entry(key, value) in self.buckets[key_index]:
            for i in range(len(self.buckets[key_index])):
                if key == self.buckets[key_index][i].get_key():
                    self.buckets[key_index][i] = self.Entry(key, value)
        elif self.buckets[key_index] is not None:
            self.buckets[key_index].append(self.Entry(key, value))

        print(self)

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return sum([1 for i in self.items()])

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.size

    def values(self):
        # TODO Должен возвращать итератор значений
        return (entry.get_value() for chain in self.buckets if chain is not None for entry in chain)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return (entry.get_key() for chain in self.buckets if chain is not None for entry in chain)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return ((entry.get_key(), entry.get_value()) for chain in self.buckets if chain is not None for entry in chain)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        new_hashmap = HashMap(3 * self.size // 2)
        for item in self.items():
            new_hashmap.put(item[0], item[1])
        self.size = new_hashmap.size
        self.buckets = new_hashmap.buckets

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f"buckets: {[i for i in self.items()]}, items: {len(self)}"

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
