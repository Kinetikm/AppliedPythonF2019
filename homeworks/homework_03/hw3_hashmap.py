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
            return self._key == other.get_key

    class Iterator:
        def __init__(self, table, type):
            self.ind_1 = 0
            self.ind_2 = 0
            self.table = []
            self.type = type
            for item in table:
                if item:
                    self.table.append(item)

        def __iter__(self):
            return self

        def return_type(self, ind_1, ind_2):
            if self.type == 'key':
                return self.table[self.ind_1][self.ind_2].get_key()
            elif self.type == 'value':
                return self.table[self.ind_1][self.ind_2].get_value()
            elif self.type == 'item':
                key = self.table[self.ind_1][self.ind_2].get_key()
                value = self.table[self.ind_1][self.ind_2].get_value()
                return (key, value)

        def __next__(self):
            while self.ind_1 < len(self.table):
                if len(self.table[self.ind_1]) >= 1:
                    if self.ind_2 < len(self.table[self.ind_1]):
                        el = self.return_type(self.ind_1, self.ind_2)
                        self.ind_2 += 1
                        return el
                self.ind_1 += 1
                self.ind_2 = 0
            raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.num_nodes = 0
        self.table = [[] for _ in range(self.bucket_num)]
        self.keys_list = []
        self.load_coeff = 0.66  # коэффициент заполнения (2/3)
        self.coeff = 4  # во сколько раз увеличивается размер таблицы

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        ind = self._get_index(self._get_hash(key))
        if not self.table[ind]:
            return default_value
        if self.__contains__(key):
            for el in self.table[ind]:
                if key == el.get_key():
                    return el.get_value()
        else:
            return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        ind = self._get_index(self._get_hash(key))
        node = self.Entry(key, value)
        if not self.table[ind]:
            self.table[ind].append(node)
            self.num_nodes += 1
            return
        if self.__contains__(key):
            for i in range(len(self.table[ind])):
                if node == self.table[ind][i]:
                    self.table[ind][i] = node
                    if self.num_nodes > self.load_coeff * self.bucket_num:
                        self._resize()
                    return
        else:
            self.table[ind].append(node)
            self.num_nodes += 1
            if self.num_nodes >= self.load_coeff*self.bucket_num:
                self._resize()
            return

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.num_nodes

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.Iterator(self.table, type='value')

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.Iterator(self.table, type='key')

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.Iterator(self.table, type='item')

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        lst_item = [i for i in self.items()]
        self.bucket_num *= self.coeff
        num_el = self.num_nodes
        #  Удаляем  table, чтобы переобозначить её элементы, предварительно скопировав их
        del self.table
        self.table = [[] for _ in range(self.bucket_num)]
        for key, value in lst_item:
            self.put(key, value)
        #  В методе put происходит увеличение num_nodes, но поскольку
        #  происходит лишь переобозначение , то нужно вернуть num_nodes к исходному значению
        self.num_nodes = num_el

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, self.num_nodes)

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        ind = self._get_index(self._get_hash(item))
        for i in self.table[ind]:
            if item == i.get_key():
                return True
