from ray import Ray
from vec3 import vec3
class Material():
    def scatter(self, r_in, rec):
        return False, None, None
    
class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo
        
    def scatter(self, r_in, rec):
        scatter_direction = rec.normal + vec3.random_unit_vector()
        if vec3.near_zero(scatter_direction):
            scatter_direction = rec.normal

        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
    
        return True, scattered, attenuation


class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = fuzz
        
    def scatter(self, r_in, rec):
        reflected = vec3.reflect(r_in.direction(), rec.normal)
        reflected = vec3.unit_vector(reflected) + (self.fuzz * vec3.random_unit_vector())
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        return  (vec3.dot(scattered.direction(), rec.normal) > 0), scattered, attenuation

class Dielectric(Material):
    def __init__(self, refraction_index):
        self.refraction_index = refraction_index

    def scatter(self, r_in, rec):
        attenuation = vec3(1.0, 1.0, 1.0)
        if rec.front_face:
            ri = (1.0/self.refraction_index)
        else:
            ri = self.refraction_index

        unit_direction = vec3.unit_vector(r_in.direction())
        refracted = vec3.refract(unit_direction, rec.normal, ri)

        scattered = Ray(rec.p, refracted)
        return True, scattered, attenuation