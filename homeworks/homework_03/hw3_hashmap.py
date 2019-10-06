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
            return self._key == other

    class IterItems:
        def __init__(self, table, keys_num):
            self._ptr = 0
            self._table = table
            self._keys_num = keys_num
            print(table)

        def __iter__(self):
            return self

        def __next__(self):
            # returns current value and increases ptr
            if self._ptr == self._keys_num:
                raise StopIteration
            lptr = self._ptr
            self._ptr += 1
            for entry_list in self._table:
                if not entry_list:
                    continue
                if lptr >= len(entry_list):
                    lptr -= len(entry_list)
                else:
                    return (entry_list[lptr].get_key, entry_list[lptr].get_value)

    class IterKeys(IterItems):
        def __next__(self):
            t = super().__next__()
            return t[0]

    class IterValues(IterItems):
        def __next__(self):
            t = super().__next__()
            return t[1]

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        # table - list: hash % bucket_num -> list of Entries
        self._bucket_num = bucket_num
        self._table = [[] for i in range(bucket_num)]
        self._filled_num = 0
        self.keys_num = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        idx = self._get_index(self._get_hash(key))
        if not self._table[idx]:
            return default_value
        for item in self._table[idx]:
            if item.get_key() == key:
                return item.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        # индекс ячейки, в которую будем класть элемент
        idx = self._get_index(self._get_hash(key))
        new_item = self.Entry(key, value)
        # запослняем новую ячейку, если она пустая
        if not self._table[idx]:
            self._table[idx].append(new_item)
            self._filled_num += 1
            self.keys_num += 1
            if self._filled_num > 0.66 * self._bucket_num:
                self._resize()
            return
        # ищем элемент в цепочке
        else:
            for item in self._table[idx]:
                if key == item.get_key():
                    item._value = new_item.get_value()
                    return
        # добавляем элемнт в цепочку
        self._table[idx].append(new_item)
        self.keys_num += 1
        return

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.keys_num

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self._bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.IterValues(self._table, self.keys_num)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.IterKeys(self._table, self.keys_num)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.IterItems(self._table, self.keys_num)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        tmp = self._table.copy()
        old_num = self._bucket_num
        # self._bucket_num += round(self._bucket_num * 0.66)
        self._bucket_num *= 2
        self._table = [[] for it in range(self._bucket_num)]
        for i in range(old_num):
            self._table[i] = tmp[i]

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self._bucket_num, self.keys_num)

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        idx = self._get_index(self._get_hash(item))
        return item in self._table[idx]
