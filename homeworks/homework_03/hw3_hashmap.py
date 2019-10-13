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
            #  возвращаем ключ
            return self._key

        def get_value(self):
            #  возвращаем значение
            return self._value

        def __eq__(self, other):
            #  реализовать функцию сравнения
            return self._key == other.get_key()

        def set_value(self, value):
            self._value = value

    class ItemIterator:
        def __init__(self, hash_map, keys):
            self.hash_map = hash_map
            self.keys = keys
            self.seek = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.seek < len(self.keys):
                self.seek += 1
                return self.keys[self.seek - 1], self.hash_map.get(self.keys[self.seek - 1])
            else:
                raise StopIteration

    class ValueIterator(ItemIterator):
        def __next__(self):
            if self.seek < len(self.keys):
                self.seek += 1
                return self.hash_map.get(self.keys[self.seek - 1])
            else:
                raise StopIteration

    class KeyIterator(ItemIterator):
        def __next__(self):
            if self.seek < len(self.keys):
                self.seek += 1
                return self.keys[self.seek - 1]
            else:
                raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.size = bucket_num
        self.hash_map = [[] for _ in range(self.size)]
        self.elem_num = 0
        self.keys_list = []
        self.LOAD_K = 0.66
        self.INCREASE = 2

    def get(self, key, default_value=None):
        #  метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        ind = self._get_index(self._get_hash(key))
        for entry in self.hash_map[ind]:
            if key == entry.get_key():
                return entry.get_value()
        return default_value

    def put(self, key, value):
        #  метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        ind = self._get_index(self._get_hash(key))
        for entry in self.hash_map[ind]:
            if entry.get_key() == key:
                entry.set_value(value)
                return None
        self.hash_map[ind].append(self.Entry(key, value))
        self.elem_num += 1
        self.keys_list.append(key)
        if self.elem_num > self.LOAD_K * self.size:
            self._resize()

    def __len__(self):
        # Возвращает количество Entry в массиве
        return self.elem_num

    def _get_hash(self, key):
        #  Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        #  По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.size

    def values(self):
        #  Должен возвращать итератор значений
        return self.ValueIterator(self, self.keys_list)

    def keys(self):
        #  Должен возвращать итератор ключей
        return self.KeyIterator(self, self.keys_list)

    def items(self):
        #  Должен возвращать итератор пар ключ и значение (tuples)
        return self.ItemIterator(self, self.keys_list)

    def _resize(self):
        #  Время от времени нужно ресайзить нашу хешмапу
        self.size *= self.INCREASE
        old_elem_num = self.elem_num
        self.elem_num = 0
        self.keys_list = []
        old_data = self.hash_map
        self.hash_map = [[] for _ in range(self.size)]
        for bucket in old_data:
            for entry in bucket:
                self.put(entry.get_key(), entry.get_value())
        self.elem_num = old_elem_num

    def __str__(self):
        #  Метод выводит "buckets: {}, items: {}"
        return f'buckets: {self.size}, items: {self.elem_num}'

    def __contains__(self, item):
        #  Метод проверяющий есть ли объект (через in)
        return item in self.keys_list
