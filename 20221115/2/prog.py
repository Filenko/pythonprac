import sys


class Num:
    def __get__(self, obj, objType=None):
        if hasattr(obj, "_val"):
            return obj._val
        else:
            obj._val = 0
            return obj._val

    def __set__(self, obj, val):
        if hasattr(val, "real"):
            obj._val = val.real
        elif hasattr(val, "__len__"):
            obj._val = len(val)

    def __delete__(self, obj):
        if hasattr(obj, "_val"):
            del obj._val


exec(sys.stdin.read())
