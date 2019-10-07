#!/usr/bin/env python
# coding: utf-8


class HashMap:
    '''
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    '''
    class Entry:
        def __init__(self, key, value):
            '''
            Сущность, которая хранит пары ключ-значение
            :param key: ключ
            :param value: значение
            '''
            self.key = key
            self.value = value
            self.next_v = None

        def get_key(self):
            # TODO возвращаем ключ
            return self.key

        def get_value(self):
            # TODO возвращаем значение
            return self.value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self.key == other.key

        def __iter__(self):
            while self is not None:
                yield self
                self = self.next_v

    def __init__(self, bucket_num=64):
        '''
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        '''
        self.entries = [None for _ in range(bucket_num)]
        self.len = 0
        self.buckets = bucket_num

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        tmp = self.entries[hash(key) % self.buckets]
        if tmp is None:
            return default_value
        else:
            while tmp is not None:
                if tmp.key == key:
                    return tmp.value
                if tmp.next_v is None:
                    return default_value
                tmp = tmp.next_v

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        tmp = self.entries[self._get_index(self._get_hash(key))]
        if tmp is None:
            tm = self.Entry(key, value)
            self.entries[hash(key) % self.buckets] = tm
            self.len += 1
            return
        while tmp is not None:
            if tmp.key == key:
                tmp.value = value
                return
            if tmp.next_v is None:
                tmp.next_v = self.Entry(key, value)
                self.len += 1
                return
            tmp = tmp.next_v

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.len

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.buckets

    def values(self):
        # TODO Должен возвращать итератор значений
        tmp = []
        for entry in self.entries:
            if entry is not None:
                tmp.append(entry.get_value())
                while entry.next_v is not None:
                    entry = entry.next_v
                    tmp.append(entry.get_value())
        return tmp

    def keys(self):
        # TODO Должен возвращать итератор ключей
        tmp = []
        for entry in self.entries:
            if entry is not None:
                tmp.append(entry.get_key())
                while entry.next_v is not None:
                    entry = entry.next_v
                    tmp.append(entry.get_key())
        return tmp

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return [(x, y) for x, y in zip(self.keys(), self.values())]

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        items = self.items()
        self.buckets *= 2
        self.len = 0
        self.entries = [None for _ in range(self.buckets)]
        for item in items:
            self.put(item[0], item[1])

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f"buckets: {self.buckets}, items: {self.len}"

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
