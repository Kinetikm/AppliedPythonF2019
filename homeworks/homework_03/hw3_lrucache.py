import time
import copy


class LRUCacheDecorator:

    class FArgs:
        def __init__(self, args, kwargs, access_time):
            self.args = args
            self.kwargs = kwargs
            self.acc_time = access_time

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
        self._ttl = ttl

    def delete_after_ttl(self, current_time):
        # cached_copy = copy.deepcopy(self._cached)
        if self._ttl and len(self._cached.keys()) == self._maxsize:
            least_used_farg = list(self._cached.keys())[0]
            if current_time - least_used_farg.acc_time > self._ttl:
                self._cached.pop(least_used_farg)

    def delete_least_used(self):
        if len(self._cached.keys()) == self._maxsize:
            # сохраняется порядок вставки, least_used на самом первом месте(давно не обновлялся)
            least_used_fargs = list(self._cached.keys())[0]
            self._cached.pop(least_used_fargs)

    def add_to_cache(self, fargs, value, curr_time):
        self.delete_least_used()
        self._cached[fargs] = value

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            current_time = time.time()
            fargs = self.FArgs(args, kwargs, current_time)
            self.delete_after_ttl(current_time)
            if fargs in self._cached:
                # достанет с старым access_time(в __eq__ and __hash__ время не учитывется)
                ans = self._cached.pop(fargs)
                # положит с новым accces_time( в конец self_cached!)
                self._cached[fargs] = ans
            else:
                ans = func(*args, **kwargs)
                self.add_to_cache(fargs, ans, current_time)
            return ans
        return wrapped
