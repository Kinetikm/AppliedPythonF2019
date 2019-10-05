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

    class IteratorOfItems:
        def __init__(self, list_of_keys, hash_map):
            self.hash_map = hash_map
            self.list = list_of_keys
            self.amount = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.amount < len(self.list):
                self.amount += 1
                return self.list[self.amount - 1], self.hash_map.get(self.list[self.amount - 1])
            else:
                raise StopIteration

    class IteratorOfKeys(IteratorOfItems):
        def __next__(self):
            if self.amount < len(self.list):
                self.amount += 1
                return self.list[self.amount - 1]
            else:
                raise StopIteration

    class IteratorOfValues(IteratorOfItems):
        def __next__(self):
            if self.amount < len(self.list):
                self.amount += 1
                return self.hash_map.get(self.list[self.amount - 1])
            else:
                raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.list_of_entries = []
        for i in range(self.bucket_num):
            self.list_of_entries.append([])
        self.list_of_keys = []
        self.elem_amount = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for el in self.list_of_entries[index]:
            if el.get_key() == key:
                return el.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        index = self._get_index(self._get_hash(key))
        cur_entry = self.Entry(key, value)
        for i, el in enumerate(self.list_of_entries[index]):
            if el.get_key() == key:
                self.list_of_entries[index][i] = cur_entry
                return None
        self.list_of_entries[index].append(cur_entry)
        self.elem_amount += 1
        self.list_of_keys.append(key)
        if self.elem_amount * 1.5 > self.bucket_num:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.elem_amount

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.IteratorOfValues(self.list_of_keys, self)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.IteratorOfKeys(self.list_of_keys, self)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.IteratorOfItems(self.list_of_keys, self)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        new_size = self.bucket_num * 4
        new_hashmap = HashMap(new_size)
        for key, value in self.items():
            new_hashmap.put(key, value)
        self.__dict__.update(new_hashmap.__dict__)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, self.__len__())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.list_of_keys
