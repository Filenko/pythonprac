from math import sqrt


class InvalidInput(Exception):
    pass


class BadTriangle(Exception):
    pass


def length(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y2 - y1) ** 2)


def st(instr):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(instr)
    except Exception:
        raise InvalidInput

    a, b, c = length(x1, y1, x2, y2), length(x2, y2, x3, y3), length(x1, y1, x3, y3)
    if max(a, b, c) > min(a + b, a + c, b + c):
        raise BadTriangle
    s = abs(0.5 * ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)))
    if s == 0:
        raise BadTriangle
    return s


while 42:
    try:
        s = st(input())
    except InvalidInput:
        print("Invalid input")
    except BadTriangle:
        print("Not a triangle")
    else:
        print(s)
        break
