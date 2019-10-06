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
            return self._key

        def get_value(self):
            return self._value

        def __eq__(self, other):
            return self._key == other.get_key

        def __iter__(self):
            yield self._key
            yield self._value

    def __init__(self, bucket_num=64):
        self.bucket_num = bucket_num
        self.vals = [[] for i in range(int(self.bucket_num))]
        self.CHECK = 0.75


    def get(self, key, default_value=None):
        indx = self._get_index(self._get_hash(key))
        for ent in self.vals[indx]:
            if ent.get_key() == key:
                return ent.get_value()
        return default_value


    def put(self, key, value):
        indx = self._get_index(self._get_hash(key))
        item = self.Entry(key, value)
        for i, ent in enumerate(self.vals[indx]):
            if ent == item:
                self.vals[indx].pop(i)
                break
        self.vals[indx].append(item)
        counter = self.bucket_num * self.CHECK

        if len([lst for lst in self.vals if lst]) > counter:
            self._resize()

    def __len__(self):
        return len(self.items())

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.bucket_num

    def values(self):
        return [ent.get_value() for ent in self.items()]

    def keys(self):
        return [ent.get_key() for ent in self.items()]

    def items(self):
        return [ent for lst_of_ent in self.vals for ent in lst_of_ent]

    def _resize(self):
        self.bucket_num *= 2
        items = self.items()
        self.vals = [[] for i in range(self.bucket_num)]
        for ent in items:
            self.put(ent.get_key(), ent.get_value())


    def __str__(self):
        return 'buckets: {}, items: {}'.format(self.bucket_num, len(self))

    def __contains__(self, item):
        return item in self.keys()
