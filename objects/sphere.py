import math

from hittable import Hittable, HitRecord
from vec3 import vec3
from interval import Interval

class Sphere(Hittable):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        
    def hit(self, r, ray_t, rec):
        rec = HitRecord() 
        oc = self.center - r.origin()
        a = r.direction().length_squared()
        h = vec3.dot(r.direction(), oc)
        c = oc.length_squared() - self.radius*self.radius

        discriminant = h*h - a*c
        if discriminant < 0:
            return False, None

        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return False, None
        

        rec.t = root
        rec.p = r.at(rec.t)
        rec.normal = (rec.p - self.center) / self.radius
        
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)

        return True, rec
    
