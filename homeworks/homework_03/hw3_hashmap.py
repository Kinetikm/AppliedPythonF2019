#!/usr/bin/env python
# coding: utf-8


class HashMap:

    class Entry:
        def __init__(self, key, value):
            self._key = key
            self._value = value

        def get_key(self):
            return self._key

        def get_value(self):
            return self._value

        def __eq__(self, other):
            return self._key == other.get_key()

        def __iter__(self):
            yield self._key
            yield self._value

    def __init__(self, bucket_num=64):
        self.bucket_num = bucket_num
        self.map_of_bucket = [[] for i in range(bucket_num)]

    def get(self, key, default_value=None):
        index = self._get_index(self._get_hash(key))
        for entry in self.map_of_bucket[index]:
            if key == entry.get_key():
                return entry.get_value()
        return default_value

    def put(self, key, value):
        indx = self._get_index(self._get_hash(key))
        put_entry = self.Entry(key, value)
        while True:
            if len(self.map_of_bucket) <= indx:
                self.map_of_bucket.append([])
            else:
                break
        if put_entry in self.map_of_bucket[indx]:
            self.map_of_bucket[indx].remove(put_entry)
        self.map_of_bucket[indx].append(put_entry)
        if (len([backet for backet in self.map_of_bucket if backet]) >
                0.5 * self.bucket_num):
            self._resize()

    def __len__(self):
        return len(self.items())

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % 10

    def values(self):
        return ([entry.get_value() for bucket in
                self.map_of_bucket for entry in bucket])

    def keys(self):
        return ([entry.get_key() for bucket in
                self.map_of_bucket for entry in bucket])

    def items(self):
        return ([(entry.get_key(), entry.get_value()) for bucket in
                self.map_of_bucket for entry in bucket])

    def _resize(self):
        self.bucket_num *= 2
        items = self.items()
        self.map_of_bucket = [[] for i in range(self.bucket_num)]
        for entry in items:
            self.put(*entry)

    def __str__(self):
        return ("buckets: {}, items: {}".
                format(self.bucket_num, len(self.items())))

    def __contains__(self, item):
        return item in self.keys()
