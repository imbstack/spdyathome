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
    """
    For the time being, if a path ends in '/', it expects an argument to follow
    """
    # FIXME: This path stuff is dumb. Do this better if time permits
    parts = route.rstrip('/1234567890')
    return method + '->' + parts


def fill_junk(size):
    return "THIS SHOULD BE BASED ON THE SIZE OF size"
