from vec3 import vec3
from objects.sphere import Sphere
from hittable_list import HittableList
from camera import Camera
from material import Dielectric, Material, Lambertian, Metal, Dielectric

aspect_ratio = 16 / 9
image_width  = 480

material_ground = Lambertian(vec3(0.8, 0.8, 0.0))
material_center = Lambertian(vec3(0.1, 0.2, 0.5))
material_left   = Dielectric(1.5)
material_bubble = Dielectric(1.00 / 1.50)
material_right  = Metal(vec3(0.8, 0.6, 0.2), 0)

cam = Camera(image_width, aspect_ratio)
world = HittableList()

world.add(Sphere(vec3( 0.0, -100.5, -1.0), 100.0, material_ground))
world.add(Sphere(vec3( 0.0,    0.0, -1.2),   0.5, material_center))
world.add(Sphere(vec3(-1.0,    0.0, -1.0),   0.5, material_left))
world.add(Sphere(vec3(-1.0,    0.0, -1.0),   0.4, material_bubble))
world.add(Sphere(vec3( 1.0,    0.0, -1.0),   0.5, material_right))

cam.render(world)