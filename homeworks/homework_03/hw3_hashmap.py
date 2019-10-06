#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
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
        def __init__(self, hash_table, type):

            self.point1 = 0
            self.point2 = 0
            self.table = hash_table
            self.type = type

        def return_this_type(self, point1, point2):
            if self.type == 'item':
                key = self.table[self.point1][self.point2].get_key()
                value = self.table[self.point1][self.point2].get_value()
                return (key, value)
            elif self.type == 'key':
                return self.table[self.point1][self.point2].get_key()
            elif self.type == 'value':
                return self.table[self.point1][self.point2].get_value()

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
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.hash_map = [[] for i in range(int(self.bucket_num))]
        self.CHECK = 0.4
        self.RESIZE = 2
        self.count_of_items = 0
        self.not_empty_buckets = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        if self.__contains__(key):
            for entry in self.hash_map[index]:
                if entry.get_key() == key:
                    return entry.get_value()
            return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        index = self._get_index(self._get_hash(key))
        item = self.Entry(key, value)
        if not self.hash_map[index]:
            self.hash_map[index].append(item)
            self.count_of_items += 1
            self.not_empty_buckets += 1
            return
        if self.__contains__(key):
            for i in range(len(self.hash_map[index])):
                if item.get_key() == self.hash_map[index][i].get_key():
                    self.hash_map[index][i] = item
                    if self.not_empty_buckets > self.CHECK * self.bucket_num:
                        self._resize()
                    return
        else:
            self.hash_map[index].append(index)
            self.count_of_items += 1
            if self.not_empty_buckets > self.CHECK * self.bucket_num:
                self._resize()
            return

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.count_of_items

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.Iterator(self.hash_map, type='value')

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.Iterator(self.hash_map, type='key')

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.Iterator(self.hash_map, type='item')

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмап
        items = [it for it in self.items()]
        self.bucket_num *= self.RESIZE
        num_elements_save = self.count_of_items
        self.hash_map = [[] for _ in range(self.bucket_num)]
        for key, value in items:
            self.put(key, value)
        self.count_of_items = num_elements_save

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, self.count_of_items)

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        index = self._get_index(self._get_hash(item))
        for elem in self.hash_map[index]:
            if item == elem.get_key():
                return True