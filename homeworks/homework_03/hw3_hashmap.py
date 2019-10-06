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
            return self.key == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        # Num of buckets
        self.NoB = bucket_num
        self.H = [[] for i in range(self.NoB)]

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        i = self._get_index(self._get_hash(key))
        for En in self.H[i]:
            if key == En.get_key():
                return En.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        i = self._get_index(self._get_hash(key))
        en = self.Entry(key, value)
        for j, En in enumerate(self.H[i]):
            if En == en:
                self.H[i].pop(j)
                break
        self.H[i].append(en)
        maxx = self.NoB*(1/3)
        if self.__len__() > maxx:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return len(self.items())

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return(hash(key))

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.NoB

    def values(self):
        # TODO Должен возвращать итератор значений
        help_list = []
        for i in range(self.NoB):
            for En in self.H[i]:
                help_list.append(En.get_value())
        return help_list

    def keys(self):
        # TODO Должен возвращать итератор ключей
        help_list = []
        for i in range(self.NoB):
            for En in self.H[i]:
                help_list.append(En.get_key())
        return help_list

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        help_list = []
        for i in range(self.NoB):
            for En in self.H[i]:
                help_list.append((En.get_key(), En.get_value()))
        return help_list

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        Entries = self.items()
        self.NoB *= 2
        self.H = [[] for i in range(self.NoB)]
        for En in Entries:
            self.put(En[0], En[1])

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}".format(self.NoB, self.__len__())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
