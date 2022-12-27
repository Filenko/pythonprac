import sys


class Alpha:
    __slots__ = [x for x in 'abcdefghijklmnopqrstuvwxyz']

    def __init__(self, **kwargs):
        for x in kwargs:
            self.__setattr__(x, kwargs[x])

    def __str__(self):
        s = ""
        for x in self.__slots__:
            if hasattr(self, x):
                s += f"{x}: " + str(self.__getattribute__(x)) + ", "
        if s:
            return s[:-2]


class AlphaQ:
    _letters = [x for x in 'abcdefghijklmnopqrstuvwxyz']

    def __init__(self, **kwargs):
        for (k, v) in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, k, v):
        if k in self._letters:
            self.__dict__[k] = v
        else:
            raise AttributeError

    def __str__(self):
        s_dict = sorted(self.__dict__.items())
        return ", ".join(f"{k}: {v}" for (k, v) in s_dict)


exec(sys.stdin.read())
