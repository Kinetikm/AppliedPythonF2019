import time
from functools import wraps
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''

        self.maxsize = maxsize
        self.ttl = ttl / 1000 if ttl is not None else ttl
        self.cach_arg = OrderedDict()

    def __call__(self, func):
        @wraps(func)
        def wrap(*args, **kwargs):
            key = (args, tuple(kwargs))
            if key not in self.cach_arg:
                result = func(*args, **kwargs)
                if len(self.cach_arg) < self.maxsize:
                    self.cach_arg[key] = [result, time.time()]
                else:
                    self.cach_arg.popitem(last=False)
                    self.cach_arg[key] = [result, time.time()]
                return result
            else:
                if not (self.ttl is None):
                    if (time.time() - self.cach_arg[key][1]) > self.ttl:
                        result = func(*args, **kwargs)
                        self.cach_arg[key] = [result, time.time()]
                        return result
                res_tmp = self.cach_arg.pop(key)[0]
                self.cach_arg[key] = [res_tmp, time.time()]
                result = self.cach_arg[key][0]
                return result

        return wrap
