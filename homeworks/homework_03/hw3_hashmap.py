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
            return self._key

        def get_value(self):
            #  возвращаем значение
            return self._value

        def __eq__(self, other):
            #  реализовать функцию сравнения
            if isinstance(other, type(self)):
                return self.get_key() == other.get_key()
            return False

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.vals = [None for i in range(bucket_num)]
        self.leng = 0

    def get(self, key, default_value=None):
        # метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        if self.vals[index] is not None:
            for entry in self.vals[index]:
                if entry.get_key() == key:
                    return entry.get_value()
        return default_value

    def put(self, key, value):
        #  метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        index = self._get_index(self._get_hash(key))
        if self.vals[index] is None:
            self.vals[index] = [self.Entry(key, value)]
            self.leng += 1
            return

        for i, entry in enumerate(self.vals[index]):
            if entry.get_key() == key:
                self.vals[index][i] = self.Entry(key, value)
                return
        self.leng += 1
        self.vals[index].insert(0, self.Entry(key, value))

    def __len__(self):
        #  Возвращает количество Entry в массиве
        return self.leng

    def _get_hash(self, key):
        # Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        #  По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        #  Должен возвращать итератор значений
        for bucket in self.vals:
            if bucket is not None:
                for entry in bucket:
                    yield entry.get_value()

    def keys(self):
        #  Должен возвращать итератор ключей
        for i in self.vals:
            if i is not None:
                for j in i:
                    yield j.get_key()

    def items(self):
        #  Должен возвращать итератор пар ключ и значение (tuples)
        for i in self.vals:
            if i is not None:
                for j in i:
                    yield (j.get_key(), j.get_value())

    def _resize(self):
        #  Время от времени нужно ресайзить нашу хешмапу
        old_vals = self.vals
        self.vals = [None for i in range(len(self.vals) * 2)]
        for bucket in old_vals:
            if bucket is not None:
                for entry in bucket:
                    index = self._get_index(self._get_hash(entry.get_key()))
                    if self.vals[index] is None:
                        self.vals[index] = [entry]
                    else:
                        self.vals = [entry].append(self.vals)

    def __str__(self):
        #  Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}"

    def __contains__(self, item):
        #  Метод проверяющий есть ли объект (через in)
        index = self._get_index(self._get_hash(item))
        if self.vals[index] is not None:
            for entry in self.vals[index]:
                if entry.get_key() == item:
                    return True
        return False
