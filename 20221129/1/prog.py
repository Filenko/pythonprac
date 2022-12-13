from functools import wraps
import sys

def dec(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        print(f'{wrapper.__name__}: {args}, {kwargs}')
        return f(self, *args, **kwargs)
    return wrapper

class dump(type):
    def __init__(cls, name, p, ns, **kwargs):
        for (k,v) in ns.items():
            if callable(v):
                setattr(cls, k, dec(v))
        super().__init__(name, p, ns)

exec(sys.stdin.read())