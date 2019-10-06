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
            self.next = None

        def get_key(self):
            # TODO возвращаем ключ
            return self.key

        def get_value(self):
            # TODO возвращаем значение
            return self.value

        def set_value(self, value):
            self.value = value

        def get_next(self):
            return self.next

        def set_next(self, other):
            self.next = other

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self.get_key() == other.get_key()

    class ItemIterator:
        """
        раз уж решили делать объектненько:)
        """
        def __init__(self, hash_map, keys):
            self._position = 0
            self._keys = keys
            self._hash_map = hash_map

        def __iter__(self):
            return self

        def __next__(self):
            if self._position == len(self._keys):
                raise StopIteration
            key = self._keys[self._position]
            value = self._hash_map.get(key)
            self._position += 1
            return key, value

    class KeyIterator(ItemIterator):
        def __next__(self):
            if self._position == len(self._keys):
                raise StopIteration
            self._position += 1
            return self._keys[self._position - 1]

    class ValuesIterator(ItemIterator):
        def __next__(self):
            if self._position == len(self._keys):
                raise StopIteration
            self._position += 1
            return self._hash_map.get(self._keys[self._position - 1])

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.hashEntryTable = []
        for i in range(self.bucket_num):
            self.hashEntryTable.append([])
        self.real_size = 0
        self._keys = []

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for i, element in enumerate(self.hashEntryTable[index]):
            if element.get_key() == key:
                return element.get_value()
        else:
            return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        entry_elem = self.Entry(key, value)
        index = self._get_index(self._get_hash(key))
        if not self.__contains__(key):
            self.hashEntryTable[index].append(entry_elem)
            self.real_size += 1
            self._keys.append(key)
        else:
            for i, element in enumerate(self.hashEntryTable[index]):
                if element == entry_elem:
                    self.hashEntryTable[index][i] = entry_elem

        if self.bucket_num / self.__len__() < 1.5:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.real_size

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.ValuesIterator(self, self._keys)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.KeyIterator(self, self._keys)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.ItemIterator(self, self._keys)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        new_bucket_num = 2 * self.bucket_num
        items = self.items()
        new_hash_map = HashMap(bucket_num=new_bucket_num)
        for item in items:
            new_hash_map.put(item[0], item[1])
        self.__dict__.update(new_hash_map.__dict__)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, self.__len__())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        index = self._get_index(self._get_hash(item))
        for i, element in enumerate(self.hashEntryTable[index]):
            if element.get_key() == item:
                return True
        return False
