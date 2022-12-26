import sys

class Grange:
    def __init__(self, b_0, q, b_n) -> None:
        self.b_0 = b_0
        self.q = q
        self.b_n = b_n

    def __len__(self):
        curb = self.b_0
        sz = 0
        while curb < self.b_n:
            curb *= self.q
            sz += 1
        return sz
    def __getitem__(self, i):
        if type(i) == int:
            return self.b_0 * (self.q**i)
        else:
            start = i.start
            end = i.stop
            step = i.step
            if not step:
                step = self.q
            else:
                step = self.q ** step
            return Grange(start, step, end)
    def __iter__(self):
        self.curb = self.b_0
        while self.curb < self.b_n:
            yield self.curb
            self.curb *= self.q

    def __str__(self):
        return f"grange({self.b_0}, {self.q}, {self.b_n})"

    def __repr__(self):
        return f"grange({self.b_0}, {self.q}, {self.b_n})"
    def __bool__(self):
        return bool(len(self))

exec(sys.stdin.read())

