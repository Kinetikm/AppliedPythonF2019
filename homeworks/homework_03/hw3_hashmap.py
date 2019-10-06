#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """

    class Iterator:

        def __init__(self, table, i_type=None):
            self._table = table
            self._type = i_type
            self._key_iterator = 0
            self._val_iterator = 0

        def __iter__(self):
            return self

        def __next__(self):
            while self._key_iterator < len(self._table):
                if self._table[self._key_iterator] and self._val_iterator < len(self._table[self._key_iterator]):
                    entry = self._table[self._key_iterator][self._val_iterator]
                    self._val_iterator += 1
                    if self._type is None:
                        return entry.get_key(), entry.get_value()
                    elif self._type == 0:
                        return entry.get_key()
                    elif self._type == 1:
                        return entry.get_value()
                self._val_iterator = 0
                self._key_iterator += 1
            raise StopIteration

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
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other):
            return self.key == other.key

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._buckets_num = bucket_num
        self._buckets_usd = 0
        self._entries_num = 0
        self._table = [None for _ in range(self._buckets_num)]

    def get(self, key, default_value=None):
        # метод get, возвращающий значение, если оно присутствует, иначе default_value
        idx = self._get_index(self._get_hash(key))
        if self._table[idx] is not None:
            for entry in self._table[idx]:
                if key == entry.get_key():
                    return entry.get_value()
        return default_value

    def put(self, key, value):
        # метод put, кладет значение по ключу, в случае, если ключ уже присутствует он его заменяет
        idx = self._get_index(self._get_hash(key))
        entry = self.Entry(key, value)
        insert = False
        if self._table[idx] is not None:
            for i in range(len(self._table[idx])):
                if key == self._table[idx][i].get_key():
                    self._table[idx][i] = entry
                    insert = True
                    break
        else:
            self._table[idx] = []
            self._buckets_usd += 1
        if not insert:
            self._table[idx].append(entry)
            self._entries_num += 1
        if self._entries_num / self._buckets_usd > 2 or self._buckets_usd / self._buckets_num > 2 / 3:
            self._resize()

    def __len__(self):
        # Возвращает количество Entry в массиве
        return self._entries_num

    def _get_hash(self, key):
        # Вернуть хеш от ключа, по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # По значению хеша вернуть индекс элемента в массиве
        return hash_value % self._buckets_num

    def values(self):
        # Должен возвращать итератор значений
        return self.Iterator(self._table, 1)

    def keys(self):
        # Должен возвращать итератор ключе
        return self.Iterator(self._table, 0)

    def items(self):
        # Должен возвращать итератор пар ключ и значение (tuples)
        return self.Iterator(self._table)

    def _resize(self):
        # Время от времени нужно ресайзить нашу хешмапу
        items = [i for i in self.items()]
        self._buckets_num *= 4
        self._table = [None for _ in range(self._buckets_num)]
        self._entries_num = 0
        for key, value in items:
            self.put(key, value)

    def __str__(self):
        # Метод выводит "buckets: {}, items: {}"
        return f'buckets: {self._buckets_num}, items: {self._entries_num}'

    def __contains__(self, item):
        # Метод проверяющий есть ли объект (через in)
        return True if self.get(item) is not None else False
