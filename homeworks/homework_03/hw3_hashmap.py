#!/usr/bin/env python
# coding: utf-8
import traceback


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
            self.entry = (key, value)

        def get_key(self):
            # TODO возвращаем ключ
            return self.entry[0]

        def get_value(self):
            # TODO возвращаем значение
            return self.entry[1]

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self.get_key() == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.capacity = bucket_num
        self.size = 0
        self.bucket_array = [[None]] * bucket_num

    def _add_to_size(self):
        self.size += 1
        if self.is_need_resize():
            self._resize()

    def is_need_resize(self):
        return self._get_load_factor() >= 0.75

    def _get_load_factor(self):
        return self.size / self.capacity

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        hash_ = self._get_hash(key)
        index = self._get_index(hash_)
        for entry in self.bucket_array[index]:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        hash_ = self._get_hash(key)
        index = self._get_index(hash_)
        new_entry = self.Entry(key, value)
        for i, entry in enumerate(self.bucket_array[index]):
            if entry is None:
                self.bucket_array[index][i] = new_entry
                self._add_to_size()
                return
            elif entry == new_entry:
                self.bucket_array[index][i] = new_entry
                return
        self.bucket_array[index].append(new_entry)
        self._add_to_size()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.size

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.capacity

    def values(self):
        # TODO Должен возвращать итератор значений
        values = []
        for bucket in self.bucket_array:
            for entry in bucket:
                if isinstance(entry, self.Entry):
                    values.append(entry.get_value())
        return values

    def keys(self):
        # TODO Должен возвращать итератор ключей
        keys = []
        for bucket in self.bucket_array:
            for entry in bucket:
                if isinstance(entry, self.Entry):
                    keys.append(entry.get_key())
        return keys

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        keys = self.keys()
        values = self.values()
        return zip(keys, values)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.capacity *= 2
        self.size = 0
        last_bucket_array = self.bucket_array
        self.bucket_array = [[None]] * self.capacity
        for bucket in last_bucket_array:
            for entry in bucket:
                if isinstance(entry, self.Entry):
                    self.put(entry.get_key(), entry.get_value())

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f'buckets: {self.capacity}, items: {self.items()}'

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        hash_ = self._get_hash(item)
        index = self._get_index(hash_)
        for entry in self.bucket_array[index]:
            if entry.get_key() == item:
                return True
        return False
