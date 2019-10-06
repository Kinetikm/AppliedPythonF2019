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
            return self.key == other.key

    class Iterator:
        def __init__(self, collection, type):
            self._collection = collection
            self._type = type
            self._cursor = 0
            self._excursor = 0

        def __iter__(self):
            return self

        def __next__(self):
            "excursor указывает на элементы цепочки для позиции(по хэшу) задаваемой cursor"
            while self._cursor < len(self._collection):
                if self._collection[self._cursor]:
                    if self._excursor < len(self._collection[self._cursor]):
                        el = self.current()
                        self._excursor += 1
                        return el
                self._cursor += 1
                self._excursor = 0
            raise StopIteration()

        def current(self):
            """
            Возвращаяем текущий элемент
            """
            if self._type == 'value':
                return self._collection[self._cursor][self._excursor].get_value()
            elif self._type == 'key':
                return self._collection[self._cursor][self._excursor].get_key()
            else:
                return (self._collection[self._cursor][self._excursor].get_key(),
                        self._collection[self._cursor][self._excursor].get_value())

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.load = 0.75
        self.numbuckets = bucket_num
        self.table = [None for i in range(self.numbuckets)]

    def get(self, key, default_value=None):
        # TODO метод get, возвраща  ющий значение,
        #  если оно присутствует, иначе default_value
        pos = self._get_index(self._get_hash(key))
        if self.table[pos] is not None:
            for entry in self.table[pos]:
                if entry.get_key() == key:
                    return entry.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        entry = self.Entry(key, value)
        pos = self._get_index(self._get_hash(key))
        if self.table[pos] is None:
            self.table[pos] = [entry]
            return
        for i in range(len(self.table[pos])):
            if self.table[pos][i].get_key() == key:
                self.table[pos][i] = entry
                return
        self.table[pos].append(entry)

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        sum = 0
        for i in self.table:
            if i is not None:
                sum += len(i)
        return sum

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.numbuckets

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.Iterator(self.table, 'value')

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.Iterator(self.table, 'key')

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.Iterator(self.table, 'pair')

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.numbuckets = self.numbuckets*2
        items = [item for item in self.items()]
        self.table = [None for i in range(self.numbuckets)]
        for pair in items:
            self.put(pair[0], pair[1])

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.numbuckets, self.__len__())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        pos = self._get_index(self._get_hash(item))
        if self.table[pos] is not None:
            for entry in self.table[pos]:
                if entry.get_key() == item:
                    return True
        return False
