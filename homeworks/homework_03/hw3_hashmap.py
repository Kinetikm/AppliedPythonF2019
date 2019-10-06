#!/usr/bin/env python
# coding: utf-8


class HashMap:

    class Iterator:
        def __init__(self, map, _type):
            self.ptr_bucket = 0
            self.ptr_entry = 0
            self.map = map
            self.type_ = _type

        def __iter__(self):
            return self

        def return_val(self, item):
            if self.type_ == 'keys':
                return item.get_key()
            elif self.type_ == 'values':
                return item.get_value()
            elif self.type_ == 'items':
                return item.get_key(), item.get_value()

        def __next__(self):
            while self.ptr_bucket < len(self.map):
                if len(self.map[self.ptr_bucket]) > 0 and self.ptr_entry < len(self.map[self.ptr_bucket]):
                    el = self.return_val(self.map[self.ptr_bucket][self.ptr_entry])
                    self.ptr_entry += 1
                    return el
                self.ptr_bucket += 1
                self.ptr_entry = 0
            raise StopIteration

    class Entry:
        def __init__(self, key, value):
            self.key = key
            self.value = value

        def get_key(self):
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other):
            return True if self.key == other.get_key() else False

    def __init__(self, bucket_num=64):
        self.len = 0
        self.bucket_num = bucket_num
        self.map = [[] for _ in range(bucket_num)]

    def get(self, key, default_value=None):
        _id = self._get_index(self._get_hash(key))
        for el in self.map[_id]:
            if el.get_key() == key:
                return el.get_value()
        return default_value

    def put(self, key, value):
        _id = self._get_index(self._get_hash(key))
        for el in self.map[_id]:
            if el.get_key() == key:
                el.value = value
                return True
        self.map[_id].append(self.Entry(key, value))
        self.len += 1
        return True

    def __len__(self):
        return self.len

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.bucket_num

    def values(self):
        return self.Iterator(self.map, 'values')

    def keys(self):
        return self.Iterator(self.map, 'keys')

    def items(self):
        return self.Iterator(self.map, 'items')

    def _resize(self):
        self.map += [None for _ in range(self.bucket_num)]
        self.bucket_num *= 2
        i = 0
        while i < self.bucket_num:
            arr = self.map[i]
            j, length = 0, len(arr)
            while j < length:
                new_id = self._get_index(self._get_hash(arr[j].get_key()))
                if new_id != i:
                    self.put(arr[j].get_key(), arr[j].get_value())
                    arr.pop(j)
                    length = len(arr)
                j += 1
            i += 1

    def __str__(self):
        return "buckets: {}, items: {}".format(self.bucket_num, self.len)

    def __contains__(self, item):
        _id = self._get_index(self._get_hash(item))
        for el in self.map[_id]:
            if el.get_key() == item:
                return True
        return False
