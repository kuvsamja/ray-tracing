import math
import sys
image_width = 400
aspect_ratio = 4 / 3
image_height = int(image_width // aspect_ratio)

class vec3():
    def __init__(self, x = 0, y = 0, z = 0):
        self.e = [x, y, z]
    def x(self):    return self.e[0]
    def y(self):    return self.e[1]
    def z(self):    return self.e[2]

    def __repr__(self):
        return f"({self.e[0], self.e[1], self.e[2]})"
    
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
        
def draw():
    with open("img.ppm", "w") as f:
        f.write(f"P3\n{image_width} {image_height}\n255\n")
        
        for j in range(image_height):
            for i in range(image_width):
                sys.stdout.write(f"{i} {j} \n")
                r = i / (image_width - 1)
                g = j / (image_height - 1)
                b = 0

                ir = int(255 * r)
                ig = int(255 * g)
                ib = int(255 * b)
            
                f.write(f"{str(ir)} {str(ig)} {str(ib)}\n")
    print("done")

def main():
    draw()

if __name__ == "__main__":
    main()