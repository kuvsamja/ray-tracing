from hittable import Hittable, HitRecord
from interval import Interval

class HittableList(Hittable):
    def __init__(self):
        self.objects = []

    def clear(self):
        self.objects = []
    def add(self, obj):
        self.objects.append(obj)
    
    def hit(self, r, ray_t, rec):
        self.temp_rec = HitRecord()
        self.hit_anything = False
        self.closest_so_far = ray_t.max

        for obj in self.objects:
            self.hit_obj, rec = obj.hit(r, Interval(ray_t.min, self.closest_so_far), rec)
            if rec is not None:
                self.hit_anything = True
                self.temp_rec = rec
                self.closest_so_far = self.temp_rec.t
            rec = self.temp_rec

        return self.hit_anything, rec