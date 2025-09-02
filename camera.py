import sys
import math

from vec3 import vec3
from ray import Ray
from objects.sphere import Sphere
from hittable import HitRecord, Hittable
from hittable_list import HittableList
from interval import Interval
import utilities

class Camera():
    def __init__(self, image_width, aspect_ratio):
        # Image
        self.image_width = image_width
        self.aspect_ratio = aspect_ratio
        self.image_height = int(self.image_width // self.aspect_ratio)
        self.samples_per_pixel = 100

        self.pixel_samples_scale = 1.0 / self.samples_per_pixel
        self.viewport_height = 2
        self.viewport_width = self.viewport_height * (self.image_width / self.image_height)
        self.focal_length = 1
        self.camera_center = vec3(0, 0, 0)

        self.viewport_u = vec3(self.viewport_width, 0, 0)
        self.viewport_v = vec3(0, -self.viewport_height, 0)

        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height

        # Calculate the location of the upper left pixel.
        self.viewport_upper_left = self.camera_center - vec3(0, 0, self.focal_length) - self.viewport_u/2 - self.viewport_v/2
        self.pixel00_loc = self.viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)


    def render(self, world):
        self.world = world

        past_percentage = -1
        percentage = -1
        with open("img.ppm", "w") as self.img:
            self.img.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
            for j in range(self.image_height):  
                # past_percentage = percentage
                # percentage = int(j / self.image_height * 100)
                # if past_percentage != percentage:
                #     sys.stdout.write(f"{percentage}\n")
                for i in range(self.image_width):
                    pixel_color = vec3(0, 0, 0)
                    self.sample = 0
                    for self.sample in range(self.samples_per_pixel):
                        self.r = self.get_ray(i, j)
                        pixel_color += self.ray_color(self.r, world)
                    
                    self.write_color(self.pixel_samples_scale * pixel_color)
                sys.stdout.write(f"{j}\n")
                    
        print("100\ndone")

    
    def ray_color(self, r, world):
        rec = HitRecord()
        hit_anything, rec = world.hit(r, Interval(0, math.inf), rec)
        if hit_anything:
            return 0.5 * (rec.normal + vec3(1, 1, 1))
        
        unit_direction = vec3.unit_vector(r.direction())
        a = 0.5*(unit_direction.y() + 1.0)
        return (1.0 - a) * vec3(1.0, 1.0, 1.0) + a * vec3(0.5, 0.7, 1.0)
        
    def write_color(self, pixel_color):
        r = pixel_color[0]
        g = pixel_color[1]
        b = pixel_color[2]

        ir = int(r * 255.999)
        ig = int(g * 255.999)
        ib = int(b * 255.999)
        self.img.write(f"{str(ir)} {str(ig)} {str(ib)}\n")

    def get_ray(self, i, j):
        # Construct a camera ray originating from the origin and directed at randomly sampled
        # point around the pixel location i, j.

        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x()) * self.pixel_delta_u) + ((j + offset.y()) * self.pixel_delta_v)

        ray_origin = self.camera_center
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)
    

    def sample_square(self):
        # Returns the vector to a random point in the [-.5,-.5]-[+.5,+.5] unit square.
        return vec3(utilities.random_double() - 0.5, utilities.random_double() - 0.5, 0)
    
