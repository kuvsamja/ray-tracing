import math

class vec3():
    def __init__(self, x = 0, y = 0, z = 0):
        self.e = [x, y, z]
    def x(self):    return self.e[0]
    def y(self):    return self.e[1]
    def z(self):    return self.e[2]

    def __repr__(self):
        return f"{self.e[0]}, {self.e[1]}, {self.e[2]}"
    
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
    
    def length_squared(self):
        return self.e[0]**2 + self.e[1]**2 + self.e[2]**2
    def length(self):
        return math.sqrt(self.length_squared())
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
