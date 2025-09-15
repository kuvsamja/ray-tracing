import math
import multiprocessing
import time

from vec3 import vec3
from ray import Ray
from objects.sphere import Sphere
from objects.plane import Plane
from hittable import HitRecord, Hittable
from hittable_list import HittableList
from material import Material, Lambertian, Metal
from interval import Interval
import utilities

def render_worker(args):
    start, end, image_width, image_height, samples_per_pixel, max_depth, camera_data, world = args
    buffer = []
    pixel00_loc, pixel_delta_u, pixel_delta_v, camera_center, defocus_angle, camera_center, defocus_disk_u, defocus_disk_v = camera_data
    # start_time = time.time()
    for j in range(start, end):
        # print(f"{k}: {j}, {time.time() - start_time}s")
        for i in range(image_width):
            pixel_color = vec3(0, 0, 0)
            for s in range(samples_per_pixel):
                r = Camera.get_ray(camera_data, i, j)
                pixel_color += Camera.ray_color_static(r, world, max_depth)
            pixel_color /= samples_per_pixel
                
            r = pixel_color[0]
            g = pixel_color[1]
            b = pixel_color[2]

            r = Camera.linear_to_gamma(r)
            g = Camera.linear_to_gamma(g)
            b = Camera.linear_to_gamma(b)

            ir = int(r * 255.999)
            ig = int(g * 255.999)
            ib = int(b * 255.999)
            buffer.append(f"{ir} {ig} {ib}\n")
    print("finished")
    return start, buffer
            

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
        num_procs = multiprocessing.cpu_count()
        chunk_size = 5  # number of rows per chunk (tune this!)

        # Pack minimal camera info to send to workers
        camera_data = (
            self.pixel00_loc, self.pixel_delta_u, self.pixel_delta_v,
            self.camera_center, self.defocus_angle, self.camera_center,
            self.defocus_disk_u, self.defocus_disk_v
        )

        # Build lots of small row-range tasks
        tasks = []
        for y in range(0, self.image_height, chunk_size):
            start = y
            end = min(y + chunk_size, self.image_height)
            tasks.append((start, end, self.image_width, self.image_height,
                          self.samples_per_pixel, self.max_depth, camera_data, world))

        buffers = []
        with multiprocessing.Pool(num_procs) as pool:
            for start, buf in pool.imap_unordered(render_worker, tasks):
                buffers.append((start, buf))

        # Re-order results by row start
        buffers.sort(key=lambda x: x[0])

        # Write image
        with open("image/img.ppm", "w") as f:
            f.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
            for i, rows in buffers:
                f.write("".join(rows))

        print("Rendering done!")
    @staticmethod
    def ray_color_static(r, world, depth):
        from hittable import HitRecord
        from interval import Interval
        rec = HitRecord()
        if depth <= 0:
            return vec3(0, 0, 0)
        hit_anything, rec = world.hit(r, Interval(0.001, math.inf), rec)
        if hit_anything:
            does_scatter, scattered, attenuation = rec.mat.scatter(r, rec)
            if does_scatter:
                return attenuation * Camera.ray_color_static(scattered, world, depth-1)
        unit_direction = vec3.unit_vector(r.direction())
        a = 0.5*(unit_direction.y() + 1.0)
        return (1.0-a)*vec3(1.0, 1.0, 1.0) + a*vec3(0.5, 0.7, 1.0)
        
    def linear_to_gamma(linear_component):
        if linear_component > 0:
            return math.sqrt(linear_component)
        return 0

    def get_ray(self, i, j):
        pixel00_loc, pixel_delta_u, pixel_delta_v, camera_center, defocus_angle, camera_center, defocus_disk_u, defocus_disk_v = self
        offset = Camera.sample_square()
        pixel_sample = pixel00_loc + ((i + offset.x()) * pixel_delta_u) + ((j + offset.y()) * pixel_delta_v)
        if defocus_angle <= 0:
            ray_origin = camera_center
        else:
            ray_origin = Camera.defocus_disk_sample(camera_center, defocus_disk_u, defocus_disk_v)
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)
    
    def defocus_disk_sample(camera_center, defocus_disk_u, defocus_disk_v):
        p = vec3.random_in_unit_disk()
        return camera_center + (p[0] * defocus_disk_u) + (p[1] * defocus_disk_v)

    def sample_square():
        # Returns the vector to a random point in the [-.5,-.5]-[+.5,+.5] unit square.
        return vec3(utilities.random_double() - 0.5, utilities.random_double() - 0.5, 0)
    
