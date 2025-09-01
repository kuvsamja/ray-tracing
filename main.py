import math
import sys

from vec3 import vec3
from ray import Ray
from objects.sphere import Sphere
from hittable import HitRecord, Hittable
from hittable_list import HittableList
from interval import Interval


def ray_color(r):
    rec = HitRecord()
    hit_anything, rec = world.hit(r, Interval(0, math.inf), rec)
    if hit_anything:
        return 0.5 * (rec.normal + vec3(1, 1, 1))
    
    unit_direction = vec3.unit_vector(r.direction())
    a = 0.5*(unit_direction.y() + 1.0)
    return (1.0 - a) * vec3(1.0, 1.0, 1.0) + a * vec3(0.5, 0.7, 1.0)
def draw():
    past_percentage = -1
    percentage = -1
    with open("img.ppm", "w") as f:
        f.write(f"P3\n{image_width} {image_height}\n255\n")
        for j in range(image_height):  
            past_percentage = percentage
            percentage = int(j / image_height * 100)
            if past_percentage != percentage:
                sys.stdout.write(f"{percentage}\n")
            for i in range(image_width):
                pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
                ray_direction = pixel_center - camera_center
                r = Ray(camera_center, ray_direction)

                pixel_color = ray_color(r)

                ir = pixel_color[0] * 255
                ig = pixel_color[1] * 255
                ib = pixel_color[2]* 255
                f.write(f"{str(ir)} {str(ig)} {str(ib)}\n")
    print("100\ndone")

#-------------------------------------------------------------------------------------------------
# Image
image_width = 400
max_width = 5000
if image_width > max_width:
    print("image width larger then the set maximum, increase 'max_width' to make bigger images")
    sys.exit()
aspect_ratio = 4 / 3
image_height = int(image_width // aspect_ratio)
if image_height == 0:
    print("image height must be more then")
    sys.exit()
# Viewport
viewport_height = 2
viewport_width = viewport_height * (image_width / image_height)
focal_length = 1
camera_center = vec3(0, 0, 0)

viewport_u = vec3(viewport_width, 0, 0)
viewport_v = vec3(0, -viewport_height, 0)

pixel_delta_u = viewport_u / image_width
pixel_delta_v = viewport_v / image_height

# Calculate the location of the upper left pixel.
viewport_upper_left = camera_center - vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2
pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)
#-------------------------------------------------------------------------------------------------




world = HittableList()

world.add(Sphere(vec3(0,0,-1), 0.5))
world.add(Sphere(vec3(0,-100.5,-1), 100))

draw()