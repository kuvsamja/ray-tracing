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

aspect_ratio = 4 / 3
image_width  = 400

cam = Camera(image_width, aspect_ratio)

world = HittableList()

world.add(Sphere(vec3(0,-100.5,-1), 100))
world.add(Sphere(vec3(0, 0, -1), 0.5))
# world.add(Plane(1, 1, 1, 100))
cam.render(world)