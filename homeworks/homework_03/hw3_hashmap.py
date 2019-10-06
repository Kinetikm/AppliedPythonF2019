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
            return self._key == other

    class ItemIterator():
        def __init__(self, map):
            self.map = map
            self.pos = 0
            self.num = 0

        def __iter__(self):
            return self

        def __next__(self):
            length = len(self.map)
            while self.pos < length:
                if len(self.map[self.pos]) > 0:
                    if self.num < len(self.map[self.pos]):
                        item = self.map[self.pos][self.num]
                        self.num += 1
                        return (item.get_key(), item.get_value())
                self.pos += 1
                self.num = 0
            raise StopIteration

    class KeyIterator(ItemIterator):
        def __next__(self):
            length = len(self.map)
            while self.pos < length:
                if len(self.map[self.pos]) > 0:
                    if self.num < len(self.map[self.pos]):
                        item = self.map[self.pos][self.num]
                        self.num += 1
                        return item.get_key()
                self.pos += 1
                self.num = 0
            raise StopIteration

    class ValueIterator(ItemIterator):
        def __next__(self):
            length = len(self.map)
            while self.pos < length:
                if len(self.map[self.pos]) > 0:
                    if self.num < len(self.map[self.pos]):
                        item = self.map[self.pos][self.num]
                        self.num += 1
                        return item.get_value()
                self.pos += 1
                self.num = 0
            raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.map = [[] for _ in range(bucket_num)]
        self.count = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        for item in self.map[self._get_index(self._get_hash(key))]:
            if item.get_key() == key:
                return item.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        entry = self.Entry(key, value)
        for i, v in enumerate(self.map[self._get_index(self._get_hash(key))]):
            if v.get_key() == key:
                if v.get_value() == value:
                    return
                self.map[self._get_index(self._get_hash(key))].pop(i)
                self.map[self._get_index(self._get_hash(key))].append(entry)
                self.count += 1
                return
        self.map[self._get_index(self._get_hash(key))].append(entry)
        self._resize()
        self.count += 1
        return

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.count

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.ValueIterator(self.map)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.KeyIterator(self.map)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.ItemIterator(self.map)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        if len(self) < (0.7 * self.bucket_num):
            return
        self.count2 = self.count
        self.bucket_num *= 3
        items = self.items()
        self.map = [[] for _ in range(self.bucket_num)]
        for key, value in items:
            self.put(key, value)
        self.count = self.count2

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}".format(self.bucket_num, len(self))

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
