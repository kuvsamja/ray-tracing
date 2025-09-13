import math

from ray import Ray
from vec3 import vec3
import utilities

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
        cos_theta = min(vec3.dot(-unit_direction, rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = ri * sin_theta > 1.0
        
        if cannot_refract or Dielectric.reflectance(cos_theta, ri) > utilities.random_double():
            direction = vec3.reflect(unit_direction, rec.normal)
        else:
            direction = vec3.refract(unit_direction, rec.normal, ri)

        scattered = Ray(rec.p, direction)
        
        return True, scattered, attenuation
    def reflectance(cosine, refraction_index):
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0*r0
        return r0 + (1-r0) * (1 - cosine)**5