import math
import numpy as np
class V3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def pure(self):
        return (self.x,self.y,self.z)
    def normalize(self):
        if self.len() != 0:
            return self/self.len()
        else:
            return V3(0,0,0)
    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    def cross(self,v):
        return V3(*np.cross(self.pure(),v.pure()))
    def clamp(self,a,b):
        return V3(
                np.clip(self.x,0,1),
                np.clip(self.y,0,1),
                np.clip(self.z,0,1)
            )
    
    def get_length(self):
      return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        
    def __add__(self, v):
      return V3(self.x + v.x, self.y + v.y, self.z + v.z)
        
    def __sub__(self, v):
      return V3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, n):
      return V3(self.x * n, self.y * n, self.z * n)
    
    __rmul__ = __mul__
 
    def __truediv__(self, n):
      return V3(self.x / n, self.y / n, self.z / n)
    
    def __eq__(self, other):
        if isinstance(other, V3):
            return self.x == other.x and self.y == other.y and self.z == other.z 
        return NotImplemented
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result        
        
    @staticmethod
    def dot(v1, v2):
        return (v1.x * v2.x + v1.y * v2.y + v1.z * v2.z)
    
    @staticmethod
    def zero():
        return V3(0,0,0)

    @staticmethod
    def one():
        return V3(1,1,1)


class V4(V3):
    def __init__(self,x,y,z,w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    def pure(self):
        return (self.x,self.y,self.z,self.w)
    def clamp(self,a,b):
        return V4(
                np.clip(self.x,0,1),
                np.clip(self.y,0,1),
                np.clip(self.z,0,1),
                np.clip(self.w,0,1)
            )
    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2)
    
    get_length = len
        
    def __add__(self, v):
      return V4(self.x + v.x, self.y + v.y, self.z + v.z, self.w + v.w)
        
    def __sub__(self, v):
      return V4(self.x - v.x, self.y - v.y, self.z - v.z, self.w - v.w)

    def __mul__(self, n):
        if type(n) == float or type(n) == int:  
            return V4(self.x * n, self.y * n, self.z * n, self.w * n)
        else:
            return NotImplemented
    
    __rmul__ = __mul__
 
    def __truediv__(self, n):
      return V4(self.x / n, self.y / n, self.z / n, self.w / n)
    
    def __eq__(self, other):
        if isinstance(other, V4):
            return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w
        return NotImplemented

    def HV3(self):
        return V3(self.x,self.y,self.z)/self.w
    @staticmethod
    def dot(v1, v2):
        return (v1.x * v2.x + v1.y * v2.y + v1.z * v2.z + v1.w * v2.w)
    
    @staticmethod
    def zero():
        return V4(0,0,0,0)

    @staticmethod
    def one():
        return V4(1,1,1,1)
