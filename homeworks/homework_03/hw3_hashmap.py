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
            self.key_ = key
            self.value_ = value

        def get_key(self):
            # возвращаем ключ
            return self.key_

        def get_value(self):
            # возвращаем значение
            return self.value_

        def __eq__(self, other):
            # реализовать функцию сравнения
            return self.key_ == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.buckets_num = bucket_num
        self.table = [[] for _ in range(self.buckets_num)]
        self.num_of_entries = 0
        self.increase_coefficient = 4
        self.load_coefficient = 0.66

    def get(self, key, default_value=None):
        #  метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        if not self.table[index]:
            return default_value
        for entry in self.table[index]:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value

    def put(self, key, value):
        #  метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        index = self._get_index(self._get_hash(key))
        boolean = True
        if not self.table[index]:
            self.table[index].append(self.Entry(key, value))
            self.num_of_entries += 1
            boolean = False
        if boolean:
            for entry in self.table[index]:
                if entry.get_key() == key:
                    entry.value_ = value
                    boolean = False
                    break
        if boolean:
            self.table[index].append(self.Entry(key, value))
            self.num_of_entries += 1

    def __len__(self):
        #  Возвращает количество Entry в массиве
        return self.num_of_entries

    def _get_hash(self, key):
        #  Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        #  По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.buckets_num

    def values(self):
        for lst in self.table:
            for entry in lst:
                yield entry.get_value()

    def keys(self):
        for lst in self.table:
            for entry in lst:
                yield entry.get_key()

    def items(self):
        for lst in self.table:
            for entry in lst:
                yield (entry.get_key(), entry.get_value())

    def _resize(self):
        if self.num_of_entries > self.buckets_num * self.load_coefficient:
            new_list = list(self.items())
            self.buckets_num *= self.increase_coefficient
            self.table = [[] for _ in range(self.buckets_num)]
            for items in new_list:
                self.put(items[0], items[1])

    def __str__(self):
        #  Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.buckets_num, self.num_of_entries)

    def __contains__(self, item):
        # Метод проверяющий есть ли объект (через in)
        index = self._get_index(self._get_hash(item))
        for entry in self.table[index]:
            if entry.get_key() == item:
                return True
        return False
