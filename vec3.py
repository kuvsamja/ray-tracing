import math
import utilities

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
        if isinstance(t, vec3):
            # component-wise multiplication
            return vec3(
                self.e[0] * t.e[0],
                self.e[1] * t.e[1],
                self.e[2] * t.e[2]
            )
        else:
            # scalar multiplication
            return vec3(
                self.e[0] * t,
                self.e[1] * t,
                self.e[2] * t
            )
    def __rmul__(self, t):
        if isinstance(t, vec3):
            # component-wise multiplication
            return vec3(
                self.e[0] * t.e[0],
                self.e[1] * t.e[1],
                self.e[2] * t.e[2]
            )
        else:
            # scalar multiplication
            return vec3(
                self.e[0] * t,
                self.e[1] * t,
                self.e[2] * t
            )
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
    
    def random(min_val = 0, max_val = 1):
        return vec3(utilities.random_double(min_val,max_val), utilities.random_double(min_val,max_val), utilities.random_double(min_val,max_val))

    def random_unit_vector():
        while True:
            p = vec3.random(-1,1)
            lensq = p.length_squared()
            if 0.0001 < lensq <= 1:
                return p / math.sqrt(lensq)
    def random_in_unit_disk():
        while True:
            p = vec3(utilities.random_double(-1,1), utilities.random_double(-1,1), 0)
            if p.length_squared() < 1:
                return p
        
        
    def random_on_hemisphere(normal):
        on_unit_sphere = vec3.random_unit_vector()
        if vec3.dot(on_unit_sphere, normal) > 0.0:
            return on_unit_sphere
        else:
            return -on_unit_sphere
        
    def reflect(v, n):
        return v - 2*vec3.dot(v,n)*n
    
    def refract(uv, n, etai_over_etat):
        cos_theta = min(vec3.dot(-uv, n), 1.0)
        r_out_perp =  etai_over_etat * (uv + cos_theta*n)
        r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
        return r_out_perp + r_out_parallel

    def near_zero(self):
        s = 0.0001
        return (abs(self.e[0]) < s) and (abs(self.e[1]) < s) and (abs(self.e[2]) < s)
    