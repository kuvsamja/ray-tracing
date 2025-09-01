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

Interval.empty = Interval(math.inf, -math.inf)
Interval.universe = Interval(-math.inf, math.inf)