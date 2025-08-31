import math
import sys


class vec3():
    def __init__(self, x = 0, y = 0, z = 0):
        self.e = [x, y, z]
    def x(self):    return self.e[0]
    def y(self):    return self.e[1]
    def z(self):    return self.e[2]

    def __repr__(self):
        return f"{self.e[0], self.e[1], self.e[2]}"
    
    def __neg__(self):  return vec3(-self.e[0], -self.e[1], -self.e[2])

    def __getitem__(self, i):  return self.e[i]
    def __setitem__(self, i, value):    self.e[i] = value


    def __iadd__(self, v):
        self.e[0] += v.e[0]
        self.e[1] += v.e[1]
        self.e[2] += v.e[2]
        return self
    def __isub__(self, v):
        self.e[0] -= v.e[0]
        self.e[1] -= v.e[1]
        self.e[2] -= v.e[2]
        return self
    
    def __imul__(self, t):
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self
    def __itruediv__(self, t):
        self.e[0] /= t
        self.e[1] /= t
        self.e[2] /= t
        return self
    
    def __add__(self, v):
        return vec3(self.e[0] + v.e[0], self.e[1] + v.e[1], self.e[2] + v.e[2])
    def __sub__(self, v):
        return vec3(self.e[0] - v.e[0], self.e[1] - v.e[1], self.e[2] - v.e[2])
    
    def __mul__(self, t):
        return vec3(self.e[0] * t, self.e[1] * t, self.e[2] * t)
    def __rmul__(self, t):
        return vec3(self.e[0] * t, self.e[1] * t, self.e[2] * t)
    def __truediv__(self, t):
        return vec3(self.e[0] / t, self.e[1] / t, self.e[2] / t)
    
    def length_sqared(self):
        return self.e[0]**2 + self.e[1]**2 + self.e[2]**2
    def length(self):
        return math.sqrt(self.length_sqared())
    def unit_vector(v):
        if v.length() == 0:
            return vec3(0, 0, 0)
        return v / v.length()

    def dot(u, v):
        return u.e[0]*v.e[0] + u.e[1]*v.e[1] + u.e[2]*v.e[2]
    def cross(u, v):
        return vec3(
            u.e[1] * v.e[2] - u.e[2] * v.e[1],
            u.e[2] * v.e[0] - u.e[0] * v.e[2],
            u.e[0] * v.e[1] - u.e[1] * v.e[0]
        )

class Ray():
    def __init__(self, orig, dir):
        self.orig = orig
        self.dir = dir
    def origin(self):
        return self.orig
    def direction(self):
        return self.dir
    def at(self, t):
        return self.orig + self.dir * t

def hit_sphere(center, radius, r):
    oc = center - r.origin()
    a = vec3.dot(r.direction(), r.direction())
    b = -2.0 * vec3.dot(r.direction(), oc)
    c = vec3.dot(oc, oc) - radius*radius

    discriminant = b*b - 4*a*c
    return discriminant >= 0


def ray_color(r):
    if hit_sphere(vec3(0, 0, -1), 0.5, r):
        return vec3(1, 0, 0)

    unit_direction = vec3.unit_vector(r.direction())
    a = 0.5*(unit_direction.y() + 1.0)
    return (1.0-a) * vec3(1.0, 1.0, 1.0) + a * vec3(0.5, 0.7, 1.0);

def draw():
    
    with open("img.ppm", "w") as f:
        f.write(f"P3\n{image_width} {image_height}\n255\n")
        
        for j in range(image_height):
            for i in range(image_width):
                sys.stdout.write(f"{i} {j} \n")
                pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
                ray_direction = pixel_center - camera_center
                r = Ray(camera_center, ray_direction)

                pixel_color = ray_color(r)

                ir = pixel_color[0] * 255
                ig = pixel_color[1] * 255
                ib = pixel_color[2]* 255
                f.write(f"{str(ir)} {str(ig)} {str(ib)}\n")
    print("done")

# Image
image_width = 720
aspect_ratio = 16 / 9
image_height = int(image_width // aspect_ratio)

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
# print(
# f"""image_width      = {image_width}
# aspect_ratio    = {aspect_ratio}
# image_height    = {image_height}
# viewport_height = {viewport_height}
# viewport_width  = {viewport_width}
# focal_length    = {focal_length}
# camera_center   = {camera_center}
# viewport_u      = {viewport_u}
# viewport_v      = {viewport_v}
# pixel_delta_u   = {pixel_delta_u}
# pixel_delta_v   = {pixel_delta_v}
# viewport_upper_left = {viewport_upper_left}
# pixel00_loc     = {pixel00_loc}""")


draw()
