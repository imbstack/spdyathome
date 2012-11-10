"""
General purpose helpers and decorators
"""


def register_all(cls):
    for methodname in dir(cls):
        method = getattr(cls, methodname)
        if hasattr(method, '_route') and hasattr(method, '_method'):
            cls.paths[make_ident(method._method, method._route)] = method


def register(method, path, *args):
    def wrapper(func):
        func._route = path
        func._method = method
        return func
    return wrapper


def make_ident(method, route):
    return method + '->' + route
