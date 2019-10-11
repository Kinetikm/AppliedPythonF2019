#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
    load_f = 0.75
    cap_coef = 2

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
            # TODO возвращаем ключ
            return self.key

        def get_value(self):
            # TODO возвращаем значение
            return self.value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            if self.key == other.get_key():
                return True
            return False

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.hashmap = [[] for _ in range(self.bucket_num)]

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for entry in self.hashmap[index]:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        index = self._get_index(self._get_hash(key))
        prm1 = 0
        new_entry = self.Entry(key, value)
        for entry in self.hashmap[index]:
            if entry == new_entry:
                self.hashmap[index].pop(prm1)
                break
            prm1 += 1
        self.hashmap[index].append(new_entry)
        if len([l for l in self.hashmap if l]) > self.load_f * self.bucket_num:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        prm = 0
        for el in self.hashmap:
            if el:
                prm += len(el)
        return prm

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return [entry[1] for entry in self.items()]

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return [entry[0] for entry in self.items()]

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        help_list = []
        for el in self.hashmap:
            for entry in el:
                help_list.append((entry.get_key(), entry.get_value()))
        return help_list

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.bucket_num *= self.cap_coef
        help_lst = self.items()
        self.hashmap = [[] for _ in range(self.bucket_num)]
        for i in help_lst:
            self.put(i[0], i[1])

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        ln = len(self.items())
        return "buckets:{}, items: {}".format(self.bucket_num, ln)

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
