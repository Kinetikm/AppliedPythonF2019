class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """

    class Entry:
        def __init__(self, key, value):
            """
            Сущность, которая хранит пары ключ-значение
            :param key: ключ
            :param value: значение
            """
            self.key = key
            self.value = value

        def get_key(self):
            """
            Возвращает ключ
            """
            return self.key

        def get_value(self):
            """
            Возвращает значение
            """
            return self.value

        def __eq__(self, other):
            """
            Сравнивает объекты по ключу
            :param other:
            """
            return self.value == other.get_key()

    def __init__(self, bucket_num=64, coef_for_resize=0.9):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.hash_table = [[] for i in range(bucket_num)]
        self.bucket_num = bucket_num
        self.bucket_count = 0
        self.coef_res = coef_for_resize

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        ind = self._get_index(self._get_hash(key))
        for entry in self.hash_table[ind]:
            if entry.get_key == key:
                return entry.get_value
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        ind = self._get_index(self._get_hash(key))
        item = self.Entry(key, value)
        if not self.__contains__(key):
            self.hash_table[ind].append(item)
            self.bucket_count += 1
        else:
            for i, elem in enumerate(self.hash_table[ind]):
                if elem == item:
                    self.hash_table[i] = item

        if self.bucket_count / self.bucket_num > self.coef_res:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return len(self.items())

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return [entry[1] for entry in self.items()]

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return [entry[0] for entry in self.items()]

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return [(entry.get_key(), entry.get_value()) for list_entry in self.hash_table for entry in list_entry]

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        new_bucket_num = 2 * self.bucket_num
        items = self.items()
        new_hash_map = HashMap(bucket_num=new_bucket_num)
        for item in items:
            new_hash_map.put(item[0], item[1])
        self.__dict__.update(new_hash_map.__dict__)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, len(self.items()))

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        for key in self.keys():
            if item == key:
                return True
        return False
