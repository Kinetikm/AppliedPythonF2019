from time import time
from collections import Hashable, OrderedDict, namedtuple
from functools import wraps


class LRUCacheDecorator:

    Entry = namedtuple('Entry', 'inf first_call')

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        if self.ttl is not None:
            self.ttl /= 1000
        self.cache = OrderedDict()

    def __get_hash(self, arg):
        if isinstance(arg, Hashable):
            return hash(arg)
        return hash(tuple(arg))

    def __get_full_hash(self, *args, **kwargs):
        h_args = ''.join([str(self.__get_hash(arg)) for arg in args])
        h_kwargs = ''.join([str(self.__get_hash(kwargs[k])) for k in kwargs])
        return h_args + ' ' + h_kwargs

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            h = self.__get_full_hash(*args, **kwargs)
            if h in self.cache:
                if (self.ttl is not None and
                   time() - self.cache[h].first_call > self.ttl):
                    self.cache[h] = self.Entry(func(*args, **kwargs), time())
                    self.cache.move_to_end(h)
                self.cache.move_to_end(h)
                return self.cache[h].inf
            if len(self.cache) == self.maxsize:
                self.cache.popitem(last=False)
            inf = func(*args, **kwargs)
            ctime = time()
            self.cache.update({h: self.Entry(inf, ctime)})
            return inf
        return wrapper
