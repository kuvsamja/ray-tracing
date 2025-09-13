import math
import time

import utilities
from vec3 import vec3
from objects.sphere import Sphere
from hittable_list import HittableList
from camera import Camera
from material import Dielectric, Material, Lambertian, Metal, Dielectric

def main():
    start_time = time.time()

    world = HittableList()
    cam = Camera()


    ground_material = Lambertian(vec3(0.5, 0.5, 0.5))
    world.add(Sphere(vec3(0,-1000,0), 1000, ground_material))
    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = utilities.random_double()
            center = vec3(a + 0.9*utilities.random_double(), 0.2, b + 0.9*utilities.random_double())

            if ((center - vec3(4, 0.2, 0)).length() > 0.9):

                if (choose_mat < 0.8):
                    albedo = vec3.random() * vec3.random()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif (choose_mat < 0.95):
                    albedo = vec3.random(0.5, 1)
                    fuzz = utilities.random_double(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))


    material1 = Dielectric(1.5)
    world.add(Sphere(vec3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(vec3(0.4, 0.2, 0.1))
    world.add(Sphere(vec3(-4, 1, 0), 1.0, material2))

    material3 = Metal(vec3(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(vec3(4, 1, 0), 1.0, material3))

    # material_ground = Lambertian(vec3(0.8, 0.8, 0.0));
    # material_center = Lambertian(vec3(0.1, 0.2, 0.5));
    # material_left   = Dielectric(1.50);
    # material_bubble = Dielectric(1.00 / 1.50);
    # material_right  = Metal(vec3(0.8, 0.6, 0.2), 0.0);

    # world.add(Sphere(vec3( 0.0, -100.5, -1.0), 100.0, material_ground));
    # world.add(Sphere(vec3( 0.0,    0.0, -1.2),   0.5, material_center));
    # world.add(Sphere(vec3(-1.0,    0.0, -1.0),   0.5, material_left));
    # world.add(Sphere(vec3(-1.0,    0.0, -1.0),   0.4, material_bubble));
    # world.add(Sphere(vec3( 1.0,    0.0, -1.0),   0.5, material_right));


    cam.aspect_ratio      = 4 / 3
    cam.image_width       = 200
    cam.samples_per_pixel = 10
    cam.max_depth         = 50


    cam.defocus_angle = 0.0
    cam.focus_dist    = 10.0

    cam.vfov     = 20
    cam.lookfrom = vec3(13,2,3)
    cam.lookat   = vec3(0,0,0)
    cam.vup      = vec3(0,1,0)

    cam.render(world)

    print(f"finished executing in {time.time() - start_time} seconds")

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()