"""
van Emde Boas tree is a data structure for fast insertion, deletion
or finding successor of a given number on {0, 1, ..., u}
in O(log(log u)) time
"""

import math


class VEBTree(object):
    __slots__ = ['size', 'sub_size', 'min', 'max', 'summary', 'clusters']

    def __init__(self, size: int):
        self.size = size
        self.sub_size = math.ceil(math.sqrt(size))
        self.min = None
        self.max = None
        if self.size > 2:
            self.summary = VEBTree(self.sub_size)
            self.clusters = [None for _ in range(self.sub_size)]

    def high(self, n: int) -> int:
        return n // self.sub_size

    def low(self, n: int) -> int:
        return n % self.sub_size

    def index(self, i: int, j: int) -> int:
        return i * self.sub_size + j

    def insert(self, x: int):
        if self.min is None:
            self.min = x
            self.max = x
            return
        if x < self.min:
            x, self.min = self.min, x
        if x > self.max:
            self.max = x
        i = self.high(x)
        if self.size <= 2:
            return
        if self.clusters[i] is None:
            self.summary.insert(i)
            self.clusters[i] = VEBTree(self.sub_size)
        self.clusters[i].insert(self.low(x))

    def delete(self, x: int):
        if self.size <= 2:
            if self.min == self.max:
                self.min = None
                self.max = None
            elif self.min == x:
                self.min = self.max
            else:
                self.max = self.min
            return
        if self.min == x:
            i = self.summary.min
            if i is None:
                self.min = None
                self.max = None
                return
            x = self.index(i, self.clusters[i].min)
            self.min = x
        self.clusters[self.high(x)].delete(self.low(x))  # recursive call
        if self.clusters[self.high(x)].min is None:
            self.summary.delete(self.high(x))  # recursive call
        if self.max == x:
            m = self.summary.max
            if m is None:
                self.max = None
            else:
                self.max = self.index(m, self.clusters[m].max)

    def successor(self, x: int) -> int:
        if self.min > x:
            return self.min
        if self.size <= 2 and self.max > x:
            return self.max
        i = self.high(x)
        if self.clusters[i] is not None and self.low(x) < self.clusters[i].max:
            j = self.clusters[i].successor(self.low(x))
        else:
            i = self.summary.successor(self.high(x))
            j = self.clusters[i].min
        return self.index(i, j)


if __name__ == '__main__':
    r = VEBTree(16)
    r.insert(2)
    r.insert(3)
    r.insert(1)
    print(r.successor(0))
    r.delete(1)
    print(r.successor(0))
    pass
