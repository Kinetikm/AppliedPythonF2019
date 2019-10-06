#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
    class Entry:
        def __init__(self, key, value):
            self._key = key
            self._value = value

        def get_key(self):
            return self._value

        def get_value(self):
            return self._key

        def __eq__(self, other):
            return self._key == other.get_key

    def __init__(self, bucket_num=64):
        self.bucket_num = bucket_num
        self.vals = [[] for i in range(bucket_num)]

    def get(self, key, default_value=None):
        indx = self._get_index(self._get_hash(key))
        for i in self.vals[indx]:
            if i.get_key() == key:
                return i.get_value()
        return default_value

    def put(self, key, value):
        indx = self._get_index(self._get_hash(key))
        while len(self.vals) < self.bucket_num:
            self.vals.append([])
        new = self.Entry(key, value)
        if new in self.vals[indx]:
            self.vals[indx].remove(new)
        self.vals[indx].append(new)
        if len([1 for i in self.vals if i]) > self.bucket_num * 0.5:
            self._resize

    def __len__(self):
        return len(self.items())

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.bucket_num

    def values(self):
        return ([l.get_value() for case in self.vals for l in case])

    def keys(self):
        return ([l.get_key() for case in self.vals for l in case])

    def items(self):
        return ([(l.get_key(), l.get_value()) for case in self.vals for s in case])

    def _resize(self):
        self.bucket_num *= 2
        entries = self.items()
        self.vals = [[] for i in range(self.bucket_num)]
        for j in entries:
            self.put(*j)

    def __str__(self):
        return 'buckets: {}, items: {}'.format(self.bucket_num, len(self))

    def __contains__(self, item):
        return item in self.keys()
