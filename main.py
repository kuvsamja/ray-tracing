import math
import sys
import random

from vec3 import vec3
from ray import Ray
from objects.sphere import Sphere
from objects.plane import Plane
from hittable import HitRecord, Hittable
from hittable_list import HittableList
from interval import Interval
from camera import Camera
from material import Dielectric, Material, Lambertian, Metal, Dielectric

aspect_ratio = 4 / 3
image_width  = 400

material_ground = Lambertian(vec3(0.8, 0.8, 0.0))
material_center = Lambertian(vec3(0.1, 0.2, 0.5))
material_left   = Dielectric(1.50)
material_right  = Metal(vec3(0.8, 0.6, 0.2), 1)

cam = Camera(image_width, aspect_ratio)

world = HittableList()

world.add(Sphere(vec3( 0.0, -100.5, -1.0), 100.0, material_ground))
world.add(Sphere(vec3( 0.0,    0.0, -1.2),   0.5, material_center))
world.add(Sphere(vec3(-1.0,    0.0, -1.0),   0.5, material_left))
world.add(Sphere(vec3( 1.0,    0.0, -1.0),   0.5, material_right))


# world.add(Sphere(vec3(0,-100.5,-1), 100))
# world.add(Sphere(vec3(0, 0, -1), 0.5))
# world.add(Plane(1, 1, 1, 100))
vec3.random()
cam.render(world)