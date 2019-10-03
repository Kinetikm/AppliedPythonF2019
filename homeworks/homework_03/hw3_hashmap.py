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
            return self.value == other.get_key()

    class ItemIterator:
        def __init__(self, hash_map):
            self.hash_map = hash_map
            self.keys = hash_map.keys_list
            self.seek = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.seek < len(self.keys):
                key = self.keys[self.seek]
                self.seek += 1
                return key, self.hash_map.get(key)
            else:
                raise StopIteration

    class ValueIterator(ItemIterator):
        def __next__(self):
            if self.seek < len(self.keys):
                key = self.keys[self.seek]
                self.seek += 1
                return self.hash_map.get(key)
            else:
                raise StopIteration

    class KeyIterator(ItemIterator):
        def __next__(self):
            if self.seek < len(self.keys):
                key = self.keys[self.seek]
                self.seek += 1
                return key
            else:
                raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.hash_map = [[] for _ in range(bucket_num)]
        self.size = bucket_num
        self.elem_num = 0
        self.keys_list = []
        self.LOAD_K = 0.66
        self.INCREASE = 2

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        ind = self._get_index(self._get_hash(key))
        if not self.hash_map[ind]:
            return default_value
        for entry in self.hash_map[ind]:
            if key == entry.get_key():
                return entry.get_value()
            return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        ind = self._get_index(self._get_hash(key))
        if not self.hash_map[ind]:
            self.elem_num += 1
            self.keys_list.append(key)
            self.hash_map[ind].append(self.Entry(key, value))
            if self.elem_num > self.LOAD_K * self.elem_num:
                self._resize()
            return None
        for i, entry in enumerate(self.hash_map[ind]):
            if entry.get_key() == key:
                self.hash_map[ind][i] = self.Entry(key, value)
                return None
        self.elem_num += 1
        self.keys_list.append(key)
        self.hash_map[ind].append(self.Entry(key, value))
        if self.elem_num > self.LOAD_K * self.elem_num:
            self._resize()
        return None

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.elem_num

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.size

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.ValueIterator(self)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.KeyIterator(self)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.ItemIterator(self)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.size *= self.INCREASE
        values = [self.get(key) for key in self.keys_list]
        old_elem_num = self.elem_num
        self.elem_num = 0
        del self.hash_map
        self.hash_map = [[] for _ in range(self.size)]
        items = zip(self.keys_list, values)
        for key, value in items:
            self.put(key, value)
        self.elem_num = old_elem_num

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f'buckets: {self.hash_map}, items: {[(key, self.get(key)) for key in self.keys_list]}'

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys_list
