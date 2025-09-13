import sys
import math

from pyautogui import pixel

from vec3 import vec3
from ray import Ray
from objects.sphere import Sphere
from objects.plane import Plane
from hittable import HitRecord, Hittable
from hittable_list import HittableList
from material import Material, Lambertian, Metal
from interval import Interval
import utilities

class Camera():
    def __init__(self):
        self.image_width = 1080
        self.aspect_ratio = 16 / 9
        self.samples_per_pixel = 1
        self.max_depth = 50

        self.vfov = 90
        self.lookfrom = vec3(0,0,0)
        self.lookat   = vec3(0,0,-1)
        self.vup      = vec3(0,1,0)
        self.defocus_angle = 0
        self.focus_dist = 10

    def render_init(self):
        # Image
        self.image_height = int(self.image_width // self.aspect_ratio)

        # Camera
        self.pixel_samples_scale = 1.0 / self.samples_per_pixel
        self.camera_center = self.lookfrom

        # Viewport
        theta = math.radians(self.vfov)
        h = math.tan(theta/2)
        self.viewport_height = 2 * h * self.focus_dist
        self.viewport_width = self.viewport_height * (self.image_width / self.image_height)

        w = vec3.unit_vector(self.lookfrom - self.lookat)
        u = vec3.unit_vector(vec3.cross(self.vup, w))
        v = vec3.cross(w, u)

        self.viewport_u = self.viewport_width * u
        self.viewport_v = self.viewport_height * -v

        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height
        self.viewport_upper_left = self.camera_center - (self.focus_dist * w) - self.viewport_u/2 - self.viewport_v/2
        self.pixel00_loc = self.viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

        defocus_radius = self.focus_dist * math.tan(math.radians(self.defocus_angle / 2))
        self.defocus_disk_u = u * defocus_radius
        self.defocus_disk_v = v * defocus_radius

    def render(self, world):
        self.render_init()
        self.world = world

        past_percentage = -1
        percentage = -1
        with open("img.ppm", "w") as self.img:
            self.img.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
            for j in range(self.image_height):
                past_percentage = percentage
                percentage = int(j / self.image_height * 100)
                if past_percentage != percentage:
                    sys.stdout.write(f"{percentage}\n")
                for i in range(self.image_width):
                    pixel_color = vec3(0, 0, 0)
                    self.sample = 0
                    for self.sample in range(self.samples_per_pixel):
                        self.r = self.get_ray(i, j)
                        pixel_color += self.ray_color(self.r, world, self.max_depth)
                    
                    self.write_color(self.pixel_samples_scale * pixel_color)
                
                    
        print("100\ndone")

    
    def ray_color(self, r, world, depth, recourses = False):
        rec = HitRecord()
        if depth <= 0:
            return vec3(0, 0, 0)
        hit_anything, rec = world.hit(r, Interval(0.001, math.inf), rec)
        if hit_anything:
            does_scatter, scattered, attenuation = rec.mat.scatter(r, rec)
            if does_scatter:
                return attenuation * self.ray_color(scattered, world, depth-1)
        # return vec3(1,1,1)
        unit_direction = vec3.unit_vector(r.direction())
        a = 0.5*(unit_direction.y() + 1.0)
        return (1.0-a)*vec3(1.0, 1.0, 1.0) + a*vec3(0.5, 0.7, 1.0)
        # hit_anything, rec = world.hit(r, Interval(0.001, math.inf), rec)
        # if hit_anything:
        #     direction = rec.normal + vec3.random_unit_vector()
        #     # direction = vec3.random_on_hemisphere(rec.normal)
        #     return 0.5 * self.ray_color(Ray(rec.p, direction), world, depth - 1, False)
        # if recourses:
        #     return vec3(1, 1, 1)
        # unit_direction = vec3.unit_vector(r.direction())
        # a = 0.5*(unit_direction.y() + 1.0)
        # return (1.0 - a) * vec3(1.0, 1.0, 1.0) + a * vec3(0.5, 0.7, 1.0)
    
    def linear_to_gamma(linear_component):
        if linear_component > 0:
            return math.sqrt(linear_component)
        return 0

    def write_color(self, pixel_color):
        r = pixel_color[0]
        g = pixel_color[1]
        b = pixel_color[2]

        r = Camera.linear_to_gamma(r)
        g = Camera.linear_to_gamma(g)
        b = Camera.linear_to_gamma(b)

        ir = int(r * 255.999)
        ig = int(g * 255.999)
        ib = int(b * 255.999)
        self.img.write(f"{str(ir)} {str(ig)} {str(ib)}\n")

    def get_ray(self, i, j):
        # Construct a camera ray originating from the origin and directed at randomly sampled
        # point around the pixel location i, j.

        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x()) * self.pixel_delta_u) + ((j + offset.y()) * self.pixel_delta_v)
        if self.defocus_angle <= 0:
            ray_origin = self.camera_center
        else:
            ray_origin = self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)
    
    def defocus_disk_sample(self):
        p = vec3.random_in_unit_disk()
        return self.camera_center + (p[0] * self.defocus_disk_u) + (p[1] * self.defocus_disk_v)

    def sample_square(self):
        # Returns the vector to a random point in the [-.5,-.5]-[+.5,+.5] unit square.
        return vec3(utilities.random_double() - 0.5, utilities.random_double() - 0.5, 0)
    
