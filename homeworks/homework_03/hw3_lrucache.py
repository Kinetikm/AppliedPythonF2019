#!/usr/bin/env python
# coding: utf-8


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache_bank = dict()

        def __call__(self, f):
            def wrapped(*args, **kwargs):
                cache = str(args) + str(kwargs)
                if cache in self.cache_bank.keys() and (time.time() - self.cache_bank[cache][1]) * 1000 < self.ttl:
                    print('from cache_bank')
                    return self.cache_bank[cache][0]
                else:
                    if len(self.cache_bank.keys()) == self.maxsize:
                        print('from function')
                        min = min(self.cache_bank.items(), key=lambda x: x[1][1])[0]
                        del[self.cache_bank[min]]
                        res = f(*args, **kwargs)
                        cur_time = time.time()
                        self.cache_bank[cache] = [res, cur_time]
                        return res
                    else:
                        print('from function')
                        res = f(*args, **kwargs)
                        cur_time = time.time()
                        self.cache_bank[cache] = [res, cur_time]
                        return res
            return wrapped
