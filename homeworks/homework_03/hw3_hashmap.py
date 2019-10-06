#!/usr/bin/env python
# coding: utf-8


class HashMap:

    class Entry:
        def __init__(self, key, value):
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

    class ItemIterator:

        def __init__(self, HashMap):
            self._i = 0
            self._j = 0
            self._hashmap = HashMap
            self._entry = 0
            self._hash_map = HashMap._hash_map

        def get_entry(self):
            if self._hash_map[self._i] is not None:
                if self._j < len(self._hash_map[self._i]):
                    entry = self._hash_map[self._i][self._j]
                    self._j += 1
                    return entry
            self._i += 1
            self._j = 0
            while (self._i < len(self._hash_map) and
                    self._hash_map[self._i] is None):
                self._i += 1
            if self._i < len(self._hash_map):
                entry = self._hash_map[self._i][self._j]
                self._j += 1
                return entry

        def __iter__(self):
            return self

        def __next__(self):
            self._entry = self.get_entry()
            if self._i == len(self._hash_map):
                raise StopIteration
            return self._entry.get_key(), self._entry.get_value()

    class KeyIterator(ItemIterator):

        def __next__(self):
            self._entry = self.get_entry()
            if self._i == len(self._hash_map):
                raise StopIteration
            return self._entry.get_key()

    class ValueIterator(ItemIterator):

        def __next__(self):
            self._entry = self.get_entry()
            if self._i == len(self._hash_map):
                raise StopIteration
            return self._entry.get_value()

    def __init__(self, bucket_num=64):
        self._hash_map = [None] * bucket_num
        self._size = bucket_num
        self._entry_num = 0
        self._filled_buckets = 0

    def get(self, key, default_value=None):
        index = self._get_index(self._get_hash(key))
        if self._hash_map[index] is not None:
            for entry in self._hash_map[index]:
                if entry.get_key() == key:
                    return entry.get_value()
        return default_value

    def put(self, key, value):
        index = self._get_index(self._get_hash(key))
        if self._hash_map[index] is None:
            self._hash_map[index] = [self.Entry(key, value)]
            self._entry_num += 1
            self._filled_buckets += 1
        else:
            for entry in self._hash_map[index]:
                if entry.get_key() == key:
                    entry._value = value
                    return
            self._hash_map[index].append(self.Entry(key, value))
            self._entry_num += 1
        if self._filled_buckets * 2 // 3 > self._size:
            self._resize

    def __len__(self):
        return self._entry_num

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self._size

    def values(self):
        return self.ValueIterator(self)

    def keys(self):
        return self.KeyIterator(self)

    def items(self):
        return self.ItemIterator(self)

    def _resize(self):
        items = self.items()
        self._size = self._size * 2
        self._hash_map = [None] * self._size
        for key, value in enumerate(items):
            self.put(key, value)

    def __str__(self):
        return f'buckets: {self._size}, items: {self._entry_num}'

    def __contains__(self, item):
        for key in self.keys():
            if item == key:
                return True
        return False
