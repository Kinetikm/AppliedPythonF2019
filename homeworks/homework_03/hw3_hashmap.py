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
            # TODO возвращаем ключ
            return self._key

        def get_value(self):
            # TODO возвращаем значение
            return self._value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self._key == other.get_key()

    class IterKeys:

        def __init__(self, maper):
            self._point = 0
            self._list_items = maper.items_list()

        def __iter__(self):
            return self

        def __next__(self):
            if self.has_next():
                self._point += 1
                return self._list_items[self._point-1].get_key()
            else:
                raise StopIteration

        def has_next(self):
            return self._point < len(self._list_items)

    class IterValues(IterKeys):

        def __next__(self):
            if self.has_next():
                self._point += 1
                return self._list_items[self._point - 1].get_value()
            else:
                raise StopIteration

    class IterItem(IterKeys):

        def __next__(self):
            if self.has_next():
                self._point += 1
                return self._list_items[self._point - 1].get_key(), self._list_items[self._point - 1].get_value()
            else:
                raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._len = 0
        self._bucket_num = bucket_num
        self._map = [[] for i in range(self._bucket_num)]
        self._when_is_full = 0.75
        self._koef = 2

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        key_to_put = self._get_hash(key) % self._bucket_num
        checker = True
        if self._map[key_to_put]:
            for i in range(len(self._map[key_to_put])):
                if self._map[key_to_put][i].get_key() == key:
                    checker = False
                    return self._map[key_to_put][i].get_value()
            if checker:
                return default_value
        else:
            return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        key_to_put = self._get_hash(key) % self._bucket_num
        elem = self.Entry(key, value)
        if self._map[key_to_put]:
            checker = True
            for i in range(len(self._map[key_to_put])):
                if elem.get_key() == self._map[key_to_put][i].get_key():
                    self._map[key_to_put][i] = elem
                    checker = False
            if checker:
                self._map[key_to_put].append(elem)
                self._len += 1
                if self._len == self._bucket_num * self._when_is_full:
                    self._resize()
        else:
            self._map[key_to_put] = [elem]
            self._len += 1
            if self._len == self._bucket_num * self._when_is_full:
                self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self._len

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self._bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.IterValues(self)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.IterKeys(self)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.IterItem(self)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self._bucket_num *= self._koef
        new_map = HashMap(self._bucket_num)
        for key in self.keys():
            new_map.put(key, self.get(key))
        self._map = new_map


    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self._bucket_num, self._len)

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()

    def items_list(self):
        list = []
        for i in range(len(self._map)):
            for j in range(len(self._map[i])):
                list.append(self._map[i][j])
        return list
