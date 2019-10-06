#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
    class Entry:
        def __init__(self, key, value):
            self.value = value
            self.key = key

        def get_key(self):
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other):
            return self.key == other.key

    def __init__(self, bucket_num=64):
        self.length = bucket_num
        self.buckets = [None]*bucket_num
        self.capacity = 0
        self.threshold = 0.70

    def get(self, key, default_value=None):
        i = self._get_index(self._get_hash(key))
        if self.buckets[i] is not None:
            for j in self.buckets[i]:
                if j.key == key:
                    return j.value
        return default_value

    def put(self, key, value):
        if key in self.keys():
            i = self._get_index(self._get_hash(key))
            if self.buckets[i]:
                for j in self.buckets[i]:
                    if j.key == key:
                        j.value = value
        else:
            i = self._get_index(self._get_hash(key))
            if self.buckets[i] is None:
                self.buckets[i] = [self.Entry(key, value)]
            else:
                self.buckets[i].append(self.Entry(key, value))
            self.capacity += 1
        if self.capacity / self.length > self.threshold:
            self._resize()

    def __len__(self):
        return self.capacity

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.length

    def _get_items(self):
        result = []
        for bucket in self.buckets:
            if bucket:
                for var in bucket:
                    result.append((var.key, var.value))
        return result

    def values(self):
        return list(map(lambda x: x[1], self._get_items()))

    def keys(self):
        return list(map(lambda x: x[0], self._get_items()))

    def items(self):
        return self._get_items()

    def _resize(self):
        self.buckets.extend([None for _ in range(self.length)])
        self.length *= 2

    def __str__(self):
        return "buckets: {}, items: {}".format(self.buckets, self.items())

    def __contains__(self, item):
        return item in self.keys()
