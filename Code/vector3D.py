import math

class vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    # scalar multiplication
    def __mul__(self, val):
        return (self.x * val, self.y * val, self.z * val)

    # returns a vector that is the cross
    def cross_product(self, other):
        return vector3D(self.y * other.z + self.z * other.y, \
            self.z * other.x + self.x * other.z, \
                self.x * other.y + self.y * other.x)

    def dot_product(self, other):
        return self.x * other.x + self.y + other.y + self.x + other.z

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    # return a normalized version of this vector
    def unit_vector(self):
        m = self.magnitude()
        if m == 0:
            return vector3D()
        return vector3D(self.x / m, self.y / m, self.z / m)

    def __str__(self):
        return "(%s, %s, %s)" % (self.x, self.y, self.z)
