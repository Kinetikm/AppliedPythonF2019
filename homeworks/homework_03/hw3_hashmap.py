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
            return self._key == other._key

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._hashtable = [None] * bucket_num
        self.size = 0
        self.capacity = bucket_num

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        ind = self._get_index(self._get_hash(key))
        if self._hashtable[ind]:
            for item in self._hashtable[ind]:
                if item.get_key() == key:
                    return item.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        ind = self._get_index(self._get_hash(key))
        new_entry = self.Entry(key, value)
        if self._hashtable[ind]:
            if new_entry in self._hashtable[ind]:
                for single in self._hashtable[ind]:
                    if single == new_entry:
                        single._value = new_entry.get_value()
            else:
                self._hashtable[ind].append(new_entry)
                self.size += 1
        else:
            self._hashtable[ind] = [new_entry]
            self.size += 1
        if self.size / self.capacity > 0.66:
            self._resize()

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
        vls = []
        for item in self.items():
            vls.append(item[1])
        return vls

    def keys(self):
        # TODO Должен возвращать итератор ключей
        ks = []
        for item in self.items():
            ks.append(item[0])
        return ks

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        itms = []
        for element in self._hashtable:
            if element:
                for single in element:
                    itms.append((single.get_key(), single.get_value()))
        return itms

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.capacity *= 2
        tmp = [None] * self.capacity
        for element in self._hashtable:
            if element:
                for single in element:
                    new_ind = self._get_index(self._get_hash(single.get_key()))
                    if not tmp[new_ind]:
                        tmp[new_ind] = []
                    tmp[new_ind].append(single)
        self._hashtable = tmp

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f"buckets: {self._hashtable}, items: {self.items()}"

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
