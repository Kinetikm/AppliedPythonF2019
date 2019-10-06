import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''

        self.maxsize = maxsize
        self.ttl = ttl
        self.cach_arg = {}

    def __call__(self, func):
        def wrap(*args, **kwargs):
            key = (args, tuple(kwargs))
            if key not in self.cach_arg:
                result = func(*args, **kwargs)
                if len(self.cach_arg) < self.maxsize:
                    self.cach_arg[key] = [result, time.time()]
                else:
                    max_time = -1
                    for k in self.cach_arg:
                        if (time.time() - self.cach_arg[k][1]) > max_time:
                            key_tmp = k
                            max_time = (time.time() - self.cach_arg[k][1])
                    self.cach_arg.pop(key_tmp)
                    self.cach_arg[key] = [result, time.time()]
                return result
            else:
                if not (self.ttl is None):
                    if (time.time() - self.cach_arg[key][1]) * 1000 > self.ttl:
                        result = func(*args, **kwargs)
                        self.cach_arg.pop(key)
                        self.cach_arg[key] = [result, time.time()]
                        return result
                self.cach_arg[key][1] = time.time()
                result = self.cach_arg[key][0]
                return result

        return wrap
