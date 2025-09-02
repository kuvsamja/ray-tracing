import math

class Interval():
    def __init__(self, min_x = math.inf, max_x = -math.inf):
        self.min = min_x
        self.max = max_x
    def size(self):
        return self.max - self.min
    def contains(self, x):
        if self.min <= x <= self.max:
            return  True
        return False
    def surrounds(self, x):
        if self.min < x < self.max:
            return  True
        return False
    def clamp(self, x):
        if (x < self.min):
            return self.min
        if (x > self.max):
            return self.max
        return x

Interval.empty = Interval(math.inf, -math.inf)
Interval.universe = Interval(-math.inf, math.inf)