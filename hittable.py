from vec3 import vec3
from material import Material

class HitRecord():
    def __init__(self):
        self.p = vec3(0, 0, 0)
        self.normal = vec3(0, 0, 0)
        self.t = 0
        self.mat = Material()

    def set_face_normal(self, r, outward_normal):
        self.front_face = vec3.dot(r.direction(), outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal
        


class Hittable():
    def hit(self, r, ray_t, rec):
        pass
