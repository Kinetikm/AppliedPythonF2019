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
            return self.key == other.get_key

    def __init__(self, bucket_num=64):
        self.array = [[] for _ in range(bucket_num)]
        self.table_size = bucket_num
        self.fill_factor = 20

    def get(self, key, default_value=None):
        idx = self._get_index(self._get_hash(key))
        for i in self.array[idx]:
            if i.get_key() == key:
                default_value = i.get_value()
        return default_value

    def put(self, key, value):
        idx = self._get_index(self._get_hash(key))
        for i in self.array[idx]:
            if i.get_key() == key:
                i.value = value
                return
        self.array[idx].append(self.Entry(key, value))
        if self.__len__() / self.table_size > self.fill_factor:
            self._resize()

    def __len__(self):
        len_ = 0
        for i in self.array:
            len_ += len(i)
        return len_

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.table_size

    def values(self):
        return (item.get_value() for bucket in self.array for item in bucket)

    def keys(self):
        return (item.get_key() for bucket in self.array for item in bucket)

    def items(self):
        return ((item.get_key(), item.get_value()) for bucket in self.array for item in bucket)

    def _resize(self):
        buckets_tmp = self.array[::]
        self.table_size = self.table_size * 2
        self.array = [[] for _ in range(self.table_size)]
        for bucket in buckets_tmp:
            for item in range(len(bucket)):
                self.put(bucket[item].get_key(), bucket[item].get_value())

    def __str__(self):
        buckets = "{"
        items = '{'
        for i in range(self.table_size):
            if len(self.array[i]) != 0:
                buckets += str(i) + ': '
                for item in self.array[i]:
                    buckets += str(item.get_key()) + ', '
                    items += str(item.get_key()) + ': ' + str(item.get_value()) + '; '
                buckets = buckets[:-2:]
                buckets += '; '
        buckets = buckets[:-2:]
        buckets += '}'
        items = items[:-2:]
        items += '}'
        return 'buckets: {buckets1}\nitems: {items1}'.format(buckets1=buckets, items1=items)

    def __contains__(self, item):
        return self.get(item.get_key()) == item
