class HashMap:

    fill_factor = 1/3
    exp_coeff = 2

    class Entry:
        def __init__(self, key, value):
            self.__key = key
            self.__value = value

        def get_key(self):
            return self.__key

        def get_value(self):
            return self.__value

        def __eq__(self, other):
            return self.__key == other.get_key()

        def __iter__(self):
            yield self.__key
            yield self.__value

    def __init__(self, bucket_num=64):
        self.bucket_num = bucket_num
        self.fill_buckets = 0
        self.map = [[] for i in range(self.bucket_num)]

    def get(self, key, default_value=None):
        idx = self._get_index(self._get_hash(key))
        for entry in self.map[idx]:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value

    def put(self, key, value):
        idx = self._get_index(self._get_hash(key))
        put_entry = self.Entry(key, value)
        flag = True
        for i, entry in enumerate(self.map[idx]):
            if entry == put_entry:
                self.map[idx].pop(i)
                flag = False
                break
        if flag:
            self.fill_buckets += 1
        self.map[idx].append(put_entry)
        control_num = self.bucket_num*self.fill_factor
        if self.fill_buckets > control_num:
            self._resize()

    def __len__(self):
        return len(self.items())

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.bucket_num

    def values(self):
        return [entry.get_value() for entry in self.items()]

    def keys(self):
        return [entry.get_key() for entry in self.items()]

    def items(self):
        return [entry for lst_of_entry in self.map for entry in lst_of_entry]

    def _resize(self):
        self.bucket_num *= self.exp_coeff
        items = self.items()
        self.map = [[] for i in range(self.bucket_num)]
        for entry in items:
            self.put(entry.get_key(), entry.get_value())

    def __str__(self):
        return 'buckets: {}, items: {}'.format(self.bucket_num, len(self))

    def __contains__(self, key):
        idx = self._get_index(self._get_hash(key))
        for entry in self.map[idx]:
            if entry.get_key() == key:
                return True
        return False
