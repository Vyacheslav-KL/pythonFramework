from time import time


class AppRoute:

    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def check_time(method):
            def dec_method(*args, **kwargs):
                start = time()
                result = method(*args, **kwargs)
                stop = time()
                delta = stop - start
                print(f'debug >>> Page "{self.name}"'
                      f' execute time {delta:2.2f} ms')
                return result
            return dec_method
        return check_time(cls)