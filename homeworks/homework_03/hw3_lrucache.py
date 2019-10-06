import time


class LRUCacheDecorator:

    class FArgs:
        def __init__(self, args, kwargs):
            self.args = args
            self.kwargs = kwargs

        def __eq__(self, other):
            return self.args == other.args and self.kwargs == other.kwargs

        def __hash__(self):
            fargs = []
            fargs.extend(self.args)
            fargs.extend(list(self.kwargs.values()))
            t_fargs = tuple(fargs)
            return hash(t_fargs)

    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        self._maxsize = maxsize
        # function args : func(args)
        self._cached = {}
        # access_time: args
        self._access_time = {}
        self._ttl = ttl

    def delete_after_ttl(self, current_time):
        ttl = self._ttl
        if ttl:
            t_delete = [time for time in self._access_time.keys() if current_time - time > ttl]
            for t in t_delete:
                fargs = self._access_time.pop(t)
                self._cached.pop(fargs)

    def update_access_time(self, fargs, curr_time):
        for time, args in self._access_time.items():
            if args == fargs:
                self._access_time.pop(time)
                break
        self._access_time[curr_time] = fargs

    def add_to_cache(self, fargs, value, curr_time):
        if len(self._cached.keys()) == self._maxsize:
            least_used = sorted(self._access_time.keys())[0]
            least_used_fargs = self._access_time.pop(least_used)
            self._cached.pop(least_used_fargs)

        self._cached[fargs] = value
        self.update_access_time(fargs, curr_time)

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            current_time = time.time()
            fargs = self.FArgs(args, kwargs)
            self.delete_after_ttl(current_time)
            if fargs in self._cached:
                self.update_access_time(fargs, current_time)
                return self._cached[fargs]
            else:
                ans = func(*args, **kwargs)
                self.add_to_cache(fargs, ans, current_time)
                return ans
        return wrapped
