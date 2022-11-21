from collections import UserString
import sys


class DivStr(UserString):
    def __init__(self, str=""):
        super().__init__(str)

    def __floordiv__(self, other):
        whole = len(self) // other
        return iter(self[i:i + whole] for i in range(0, whole * other, whole))

    def __mod__(self, other):
        remainder = len(self) % other
        return self[-remainder:]


exec(sys.stdin.read())
