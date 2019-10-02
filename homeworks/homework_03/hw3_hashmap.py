#!/usr/bin/env python
# coding: utf-8
from typing import List


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
            # возвращаем ключ
            return self._key

        def get_value(self):
            # возвращаем значение
            return self._value

        def set_value(self, value):
            self._value = value

        def __eq__(self, other):
            # функция сравнения
            return self._key == other.get_key()

    class ItemIterator:

        def __init__(self, hash_table: 'HashMap', keys: List):
            self._cursor = 0
            self._hash_table = hash_table
            self._keys = keys

        def __iter__(self):
            return self

        def __next__(self):
            if self._cursor == len(self._keys):
                raise StopIteration
            key = self._keys[self._cursor]
            value = self._hash_table.get(key)
            self._cursor += 1
            return key, value

    class KeyIterator(ItemIterator):

        def __next__(self):
            if self._cursor == len(self._keys):
                raise StopIteration
            key = self._keys[self._cursor]
            self._cursor += 1
            return key

    class ValueIterator(ItemIterator):

        def __next__(self):
            if self._cursor == len(self._keys):
                raise StopIteration
            key = self._keys[self._cursor]
            value = self._hash_table.get(key)
            self._cursor += 1
            return value

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._table = [[] for _ in range(bucket_num)]
        self._num_element = 0  # число элементов в таблице
        self._table_size = bucket_num
        self._keys_list = []  # список ключей (нужен для итераторов)
        self._SCALE_COEFFICIENT = 4
        self._SCALE_COEFFICIENT_BOUNDARY = 5*10e4

    def get(self, key, default_value=None):
        """метод get, возвращающий значение, если оно присутствует, иначе default_value"""
        index = self._get_index(self._get_hash(key))
        if not self._table[index]:
            return default_value
        for item in self._table[index]:
            if item.get_key() == key:
                return item.get_value()
        return default_value

    def put(self, key, value):
        """ метод put, кладет значение по ключу, в случае, если ключ уже присутствует он его заменяет"""
        index = self._get_index(self._get_hash(key))
        if not self._table[index]:
            # ячейка пустая, заполняем
            self._table[index].append(self.Entry(key, value))
            self._num_element += 1
            self._keys_list.append(key)
            return
        # в ячейки уже что-то есть, идем по цепочке
        for item in self._table[index]:
            if item.get_key() == key:
                # такой ключ уже есть, заменяем
                item.set_value(value)
                return
        # прошли по цепочке, ключа нет, добавляем
        self._table[index].append(self.Entry(key, value))
        self._num_element += 1
        self._keys_list.append(key)
        if self._num_element > 0.66 * self._table_size:
            self._resize()

    def __len__(self):
        """ Возвращает количество Entry в массиве """
        return self._num_element

    def _get_hash(self, key):
        """возвращает хеш от ключа, по которому он кладется в бакет"""
        return hash(key)

    def _get_index(self, hash_value):
        """По значению хеша возвращает индекс элемента в массиве"""
        return hash_value % self._table_size

    def values(self):
        """"возвращает итератор значений"""
        return self.ValueIterator(self, self._keys_list)

    def keys(self):
        """возвращает итератор ключей"""
        return self.KeyIterator(self, self._keys_list)

    def items(self):
        """ возвращает итератор пар ключ и значение (tuples) """
        return self.ItemIterator(self, self._keys_list)

    def _resize(self):
        """Время от времени нужно ресайзить нашу хешмапу"""
        factor = self._SCALE_COEFFICIENT
        if self._table_size > self._SCALE_COEFFICIENT_BOUNDARY:
            factor = round(self._SCALE_COEFFICIENT/2)
        new_table_size = self._table_size*factor
        new_table = HashMap(bucket_num=new_table_size)
        for key, value in self.items():
            new_table.put(key, value)
        self.__dict__.update(new_table.__dict__)  # заменяем "внутренности" новыми. Не уверен, насколько хорошо
        #  так делать, но способа лучше как подменить экземпляр объекта не придумал. Менять существующий
        #  получается громоздко

    def __str__(self):
        """Метод выводит 'buckets: {}, items: {}'"""
        return 'buckets: {table}, items: {items}'.format(table=str(self._table),
                                                         items=[(key, self.get(key)) for key in self._keys_list])

    def __contains__(self, item):
        """Метод проверяющий есть ли объект (через in)"""
        return item in self._keys_list
