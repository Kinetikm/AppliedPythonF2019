from time import time
from collections import Hashable


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}

    def __get_hash(self, arg):
        if isinstance(arg, Hashable):
            return hash(arg)
        else:
            return hash(tuple(arg))

    def __full_hash(self, *args, **kwargs):
        hash = str()
        for arg in args:
            hash += str(self.__get_hash(arg))
        for key in kwargs:
            hash += str(self.__get_hash(kwargs[key]))
        return hash

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            h = self.__full_hash(*args, **kwargs)
            if h in self.cache:
                if (self.ttl is not None and
                   (time() - self.cache[h][0]) * 1000 > self.ttl):
                    self.cache[h][1] = func(*args, **kwargs)
                    self.cache[h][0] = time()
                    self.cache[h][2] = self.cache[h][0]
                    return self.cache[h][1]
                else:
                    self.cache[h][2] = time()
                    return self.cache[h][1]
            if len(self.cache) >= self.maxsize:
                time_min = time()
                key_min = None
                for key in self.cache:
                    if self.cache[key][2] <= time_min:
                        time_min = self.cache[key][2]
                        key_min = key
                self.cache.pop(key_min)

            inf = func(*args, **kwargs)
            ctime = time()
            self.cache.update({h: [ctime, inf, ctime]})
            return inf
        return wrapper
