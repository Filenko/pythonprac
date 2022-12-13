from math import sqrt


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.a = sqrt(abs(p1[0] - p2[0]) ** 2 + abs(p1[1] - p2[1]) ** 2)
        self.b = sqrt(abs(p2[0] - p3[0]) ** 2 + abs(p2[1] - p3[1]) ** 2)
        self.c = sqrt(abs(p1[0] - p3[0]) ** 2 + abs(p1[1] - p3[1]) ** 2)

    def __abs__(self):
        p = 0.5 * (self.a + self.b + self.c)
        s = sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
        return s

    def __bool__(self):
        return bool(abs(self))

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __contains__(self, item):

        def vect(x1, y1, x2, y2):
            return x1 * y2 - y1 * x2

        if type(item) is tuple:
            x0, y0 = item
            xa, ya = self.p1
            xb, yb = self.p2
            xc, yc = self.p3

            p = vect(xa - x0, ya - y0, xb - xa, yb - ya)
            q = vect(xb - x0, yb - y0, xc - xb, yc - yb)
            r = vect(xc - x0, yc - y0, xa - xc, ya - yc)

            return p * q >= 0 and q * r >= 0 and p * r >= 0

        elif item.__class__ == Triangle:
            return item.p1 in self and item.p2 in self and item.p3 in self if item else True

    def __and__(self, other):
        def isct(other, self):
            return (other not in self) and (other.p1 in self or other.p2 in self or other.p3 in self)

        return bool(self) and bool(other) and (isct(self, other) or isct(other, self))



exec(sys.stdin.read())