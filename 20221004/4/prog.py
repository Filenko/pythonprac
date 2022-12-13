from math import *


def Calc(s, t, u):
    def f():
        eval(s)
        y = eval(t)
        return eval(u)

    return f


args = eval(input())
x = eval(input())
print(Calc(*args)())
