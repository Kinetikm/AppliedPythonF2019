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
            self.__key = key
            self.__value = value

        def get_key(self):
            # TODO возвращаем ключ
            return self.__key

        def get_value(self):
            # TODO возвращаем значение
            return self.__value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            if isinstance(other, type(self)):
                return self.get_key() == other.get_key()
            return False

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.chain = [None for i in range(bucket_num)]

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        if self.chain[index] is not None:
            for i in self.chain[index]:
                if i.get_key() == key:
                    return i.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        pos = self._get_index(self._get_hash(key))
        if self.chain[pos] is None:
            self.chain[pos] = [self.Entry(key, value)]
            return
        for i, en in enumerate(self.chain[pos]):
            if en.get_key() == key:
                self.chain[pos][i] = self.Entry(key, value)
                return
        self.chain[pos] += [self.Entry(key, value)]

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        length = 0
        for bucket in self.chain:
            if bucket is not None:
                length += len(bucket)
        return length

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        for bucket in self.chain:
            if bucket is not None:
                for en in bucket:
                    yield en.get_value()

    def keys(self):
        # TODO Должен возвращать итератор ключей
        for i in self.chain:
            if i is not None:
                for j in i:
                    yield j.get_key()

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        for i in self.chain:
            if i is not None:
                for j in i:
                    yield (j.get_key(), j.get_value())

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        old = self.chain
        self.chain = [None for i in range(len(self.chain) * 2)]
        for bucket in old:
            if bucket is not None:
                for en in bucket:
                    i = self._get_index(self._get_hash(en.get_key()))
                    if self.chain[i] is None:
                        self.chain[i] = [en]
                    else:
                        self.chain = [en].append(self.chain)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}"

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        i = self._get_index(self._get_hash(item))
        if self.chain[i] is not None:
            for entry in self.chain[i]:
                if entry.get_key() == item:
                    return True
        return False
