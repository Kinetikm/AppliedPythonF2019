#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
    class ItemIterator:
        def __init__(self, hash_table):
            self._hash_table = hash_table
            self._ind = [0, -1]

        def __iter__(self):
            return self

        def __next__(self):
            if self._ind[0] < len(self._hash_table):
                if self._hash_table[self._ind[0]]:
                    if self._ind[1] + 1 < len(self._hash_table[self._ind[0]]):
                        self._ind[1] += 1
                        entry = self._hash_table[self._ind[0]][self._ind[1]]
                        return (entry.get_key(), entry.get_value())
                self._ind[0] += 1
                if self._ind[0] >= len(self._hash_table):
                        raise StopIteration
                while not self._hash_table[self._ind[0]]:
                    self._ind[0] += 1
                    if self._ind[0] >= len(self._hash_table):
                        raise StopIteration
                self._ind[1] = 0
                entry = self._hash_table[self._ind[0]][self._ind[1]]
                return (entry.get_key(), entry.get_value())
            raise StopIteration

    class KeyIterator(ItemIterator):
        def __next__(self):
            entry = super().__next__()
            return entry[0]

    class ValueIterator(ItemIterator):
        def __next__(self):
            entry = super().__next__()
            return entry[1]

    class Entry:
        def __init__(self, key, value):
            self._key = key
            self._value = value

        def get_key(self):
            return self._key

        def get_value(self):
            return self._value

        def __eq__(self, other):
            return self._key == other._key

    def __init__(self, bucket_num=10):
        self._bucket_num = bucket_num
        self._hash_table = [None] * bucket_num
        self._num = 0

    def get(self, key, default_value=None):
        k = self._get_index(self._get_hash(key))
        if self._hash_table[k]:
            for item in self._hash_table[k]:
                if item.get_key() == key:
                    return item.get_value()
        return default_value

    def put(self, key, value):
        if (self._num + 1) / self._bucket_num > 2 / 3:
            self._resize()
        ind = self._get_index(self._get_hash(key))
        if self._hash_table[ind]:
            for i in range(len(self._hash_table[ind])):
                if self._hash_table[ind][i].get_key() == key:
                    self._hash_table[ind][i]._value = value
                    return
                elif i == len(self._hash_table[ind]) - 1:
                    self._hash_table[ind].append(self.Entry(key, value))
        else:
            self._hash_table[ind] = [self.Entry(key, value)]
            self._num += 1

    def __len__(self):
        count = 0
        for i in range(self._bucket_num):
            if self._hash_table[i]:
                count += len(self._hash_table[i])
        return count

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self._bucket_num

    def values(self):
        return self.ValueIterator(self._hash_table)

    def keys(self):
        return self.KeyIterator(self._hash_table)

    def items(self):
        return self.ItemIterator(self._hash_table)

    def _resize(self):
        itr = self.items()
        self._bucket_num *= 2
        self._hash_table = [None] * self._bucket_num
        for it in itr:
            self.put(it[0], it[1])

    def __str__(self):
        return f"buckets: {self._bucket_num}, items: {len(self._hash_table)}"

    def __contains__(self, item):
        for lst in self._hash_table:
            if lst:
                for entry in lst:
                    if entry.get_key() == item:
                        return True
        return False
