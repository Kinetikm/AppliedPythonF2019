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

    class Special_Iterator:

        def __iter__(self):
            return self

        def __init__(self, some_list, need):
            self.some_list = some_list
            self.counter1 = 0
            self.counter2 = 0
            self.need = need

        def __next__(self):

            while self.counter1 < len(self.some_list):
                if self.some_list[self.counter1] != []:
                    if len(self.some_list[self.counter1]) == 1:
                        z = self.some_list[self.counter1][self.counter2]
                        self.counter2 = 0
                        self.counter1 += 1
                        if self.need == 'keys':
                            return z.get_key()
                        elif self.need == 'values':
                            return z.get_value()
                        elif self.need == 'items':
                            return z.get_key(), z.get_value()
                    else:
                        if self.counter2 < len(self.some_list[self.counter1]):
                            z = self.some_list[self.counter1][self.counter2]
                            self.counter2 += 1
                            if self.need == 'keys':
                                return z.get_key()
                            elif self.need == 'values':
                                return z.get_value()
                            elif self.need == 'items':
                                return z.get_key(), z.get_value()
                        else:
                            self.counter1 += 1
                            self.counter2 = 0

                else:
                    self.counter1 += 1
            raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        slots = []
        for i in range(self.bucket_num):
            slots.append([])
        self.slots = slots
        self.keys_list = []

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        if key in self.keys_list:
            for x in self.slots[self._get_index(self._get_hash(key))]:
                if x.get_key() == key:
                    return x.get_value()
        else:
            return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        i = 0
        for bucket in self.slots:
            if bucket != []:
                i += 1
                break
        if i == 0:
            self._resize()

        item = self.Entry(key, value)
        if self.__contains__(key):
            for x in self.slots[self._get_index(self._get_hash(item.get_key()))]:
                if x.get_key() == item.get_key():
                    x.value = item.get_value()
        else:
            self.slots[self._get_index(self._get_hash(item.get_key()))].append(item)
            self.keys_list.append(item.get_key())

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        l = 0
        for item in self.items():
            l += 1
        return l

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.Special_Iterator(self.slots, 'values')

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.Special_Iterator(self.slots, 'keys')

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.Special_Iterator(self.slots, 'items')

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        M = []
        for x in self.items():
            M.append(x)
        self.bucket_num *= 2
        slots = []
        for i in range(self.bucket_num):
            slots.append([])
        self.slots = slots
        for item in M:
            self.put(item[0], item[1])

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f'buckets: {{{self.bucket_num}}}, items: {{{self.__len__()}}}'

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys_list
