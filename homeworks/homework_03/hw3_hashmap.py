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
            return self._key == other.get_key()

    class Iterator:
        def __init__(self, table, it_type):
            self._table = table
            self._type = it_type
            self._cursor1 = 0
            self._cursor2 = 0

        def __iter__(self):
            return self

        def __next__(self):
            while self._cursor1 < len(self._table):
                if self._cursor2 < len(self._table[self._cursor1]):
                    element = self._table[self._cursor1][self._cursor2]
                    if self._type == 'keys':
                        element = element.get_key()
                    elif self._type == 'values':
                        element = element.get_value()
                    else:
                        element = (element.get_key(), element.get_value())
                    self._cursor2 += 1
                    return element
                self._cursor1 += 1
                self._cursor2 = 0
            raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._bucket_num = bucket_num
        self._num_entries = 0
        self._table = [[] for _ in range(self._bucket_num)]
        self._num_full_optimism = 0
        self._growth_coeff = 4
        self._coeff_full = 0.8

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        ind = self._get_index(self._get_hash(key))
        for ell in self._table[ind]:
            if key == ell.get_key():
                return ell.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        ind = self._get_index(self._get_hash(key))
        entry = self.Entry(key, value)
        if not self._table[ind]:
            self._table[ind].append(entry)
            self._num_entries += 1
            self._num_full_optimism += 1
            return
        for i in range(len(self._table[ind])):
            if entry.get_key() == self._table[ind][i].get_key():
                self._table[ind][i] = entry
                if self._num_full_optimism > self._coeff_full * self._bucket_num:
                    self._resize()
                return
        self._table[ind].append(entry)
        self._num_entries += 1
        if self._num_full_optimism > self._coeff_full * self._bucket_num:
            self._resize()
        return

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self._num_entries

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self._bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.Iterator(self._table, 'values')

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.Iterator(self._table, 'keys')

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.Iterator(self._table, 'items')

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        items = [it for it in self.items()]
        self._bucket_num *= self._growth_coeff
        saved_elements = self._num_entries
        self._table = [[] for _ in range(self._bucket_num)]
        for key, value in items:
            self.put(key, value)
        self._num_entries = saved_elements

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self._bucket_num, self._num_entries)

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        ind = self._get_index(self._get_hash(item))
        for ell in self._table[ind]:
            if item == ell.get_key():
                return True
        return False
