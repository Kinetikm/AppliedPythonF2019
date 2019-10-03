#!/usr/bin/env python
# coding: utf-8


class HashMap:

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
        self.map = [None for _ in range(bucket_num)]

    def get(self, key, default_value=None):
        _id = self._get_index(self._get_hash(key))
        arr = self.map[_id]
        if arr is None:
            return default_value
        else:
            for el in arr:
                if el.get_key() == key:
                    return el.get_value()
            return default_value

    def put(self, key, value):
        _id = self._get_index(self._get_hash(key))
        arr = self.map[_id]
        if arr is None:
            self.map[_id] = [self.Entry(key, value)]
            self.len += 1
            return True
        else:
            for el in arr:
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
        val_list = []
        for arr in self.map:
            if arr is None:
                continue
            for el in arr:
                val_list.append(el.get_value())
        return val_list

    def keys(self):
        key_list = []
        for arr in self.map:
            if arr is None:
                continue
            for el in arr:
                key_list.append(el.get_key())
        return key_list

    def items(self):
        items_list = []
        for arr in self.map:
            if arr is None:
                continue
            for el in arr:
                items_list.append((el.get_key(), el.get_value()))
        return items_list

    def _resize(self):
        self.map += [None for _ in range(self.bucket_num)]
        self.bucket_num *= 2
        i = 0
        while i < self.bucket_num:
            arr = self.map[i]
            if arr is not None:
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
        # TODO Метод выводит "buckets: {}, items: {}"
        raise NotImplementedError

    def __contains__(self, item):
        _id = self._get_index(self._get_hash(item))
        arr = self.map[_id]
        if arr is None:
            return False
        else:
            for el in arr:
                if el.get_key() == item:
                    return True
            return False
