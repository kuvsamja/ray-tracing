import math

from hittable import Hittable, HitRecord
from vec3 import vec3
from interval import Interval
from ray import Ray

class Plane(Hittable):
    def __init__(self, a, b, c, n):
        self.a = a
        self.b = b
        self.c = c
        self.n = n
        self.normal = vec3.unit_vector(vec3(a, b, c))
        
    def hit(self, r, ray_t, rec):
        rec = HitRecord()
        x0 = r.origin()[0]
        x1 = r.direction()[0]
        y0 = r.origin()[1]
        y1 = r.direction()[1]
        z0 = r.origin()[2]
        z1 = r.direction()[2]
        temp_a = self.a*x0 + self.b*y0 + self.c*z0 - self.n
        temp_b = self.a*x1 + self.b*y1 + self.c*z1
        if temp_b == 0:
            return False, rec
        t = -(temp_a / temp_b)

        rec.t = t
        rec.p = r.at(t)
        rec.normal = self.normal

        hit_anything = False
        if t > 0:
            hit_anything = True
        return hit_anything, rec