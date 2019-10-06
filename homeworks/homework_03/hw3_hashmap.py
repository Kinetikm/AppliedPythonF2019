#!/usr/bin/env python
# coding: utf-8


class HashMap:
    class Entry:
        def __init__(self, key, value):
            self._key = key
            self._value = value

        def get_key(self):
            return self._key

        def get_value(self):
            return self._value

        def __eq__(self, other):
            return self._key == other.get_key()

    class Iterator:
        def __init__(self, table_table, type):
            self.point1 = 0
            self.point2 = 0
            self.table = table_table
            self.type = type

        def return_this_type(self, point1, point2):
            if self.type == 'key':
                return self.table[self.point1][self.point2].get_key()
            elif self.type == 'value':
                return self.table[self.point1][self.point2].get_value()
            elif self.type == 'item':
                key = self.table[self.point1][self.point2].get_key()
                value = self.table[self.point1][self.point2].get_value()
                return (key, value)

        def __iter__(self):
            return self

        def __next__(self):
            while self.point1 < len(self.table):
                if len(self.table[self.point1]) >= 1:
                    if self.point2 < len(self.table[self.point1]):
                        element = self.return_this_type(self.point1, self.point2)
                        self.point2 += 1
                        return element
                self.point1 += 1
                self.point2 = 0
            raise StopIteration

    def __init__(self, bucket_num=64):
        self.bucket_num = bucket_num
        self.count_of_items = 0  # количество Entry в массиве
        self.not_empty_buckets = 0
        self.hash_table = [[] for i in range(self.bucket_num)]  # задаем начальную пустую таблицу
        self.CHECK = 0.4  # коэффициент заполнения (2/3)
        self.RESIZE = 2  # во сколько раз будем увеличивать размер таблицы

    def get(self, key, default_value=None):
        # индекс ячейки, в которой будем искать элемент
        index = self._get_index(self._get_hash(key))
        if self.__contains__(key):
            for elem in self.hash_table[index]:
                if key == elem.get_key():
                    return elem.get_value()
        return default_value

    def put(self, key, value):
        index = self._get_index(self._get_hash(key))
        item = self.Entry(key, value)
        if not self.hash_table[index]:
            self.hash_table[index].append(item)
            self.count_of_items += 1
            self.not_empty_buckets += 1
            return
        if self.__contains__(key):
            for i in range(len(self.hash_table[index])):
                if item.get_key() == self.hash_table[index][i].get_key():
                    self.hash_table[index][i] = item
                    if self.not_empty_buckets > self.CHECK * self.bucket_num:
                        self._resize()
                    return
        else:
            self.hash_table[index].append(item)
            self.count_of_items += 1
            if self.not_empty_buckets > self.CHECK * self.bucket_num:
                self._resize()
            return

    def __len__(self):
        return self.count_of_items

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.bucket_num

    def values(self):
        return self.Iterator(self.hash_table, type='value')

    def keys(self):
        return self.Iterator(self.hash_table, type='key')

    def items(self):
        return self.Iterator(self.hash_table, type='item')

    def _resize(self):
        items = [it for it in self.items()]
        self.bucket_num *= self.RESIZE
        num_elements_save = self.count_of_items
        self.hash_table = [[] for _ in range(self.bucket_num)]
        for key, value in items:
            self.put(key, value)
        self.count_of_items = num_elements_save

    def __str__(self):
        return 'buckets: {}, items: {}'.format(self.bucket_num, self.count_of_items)

    def __contains__(self, item):
        idx = self._get_index(self._get_hash(item))
        for elem in self.hash_table[idx]:
            if item == elem.get_key():
                return True
