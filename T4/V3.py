class V3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def pure(self):
        return (self.x,self.y,self.z)
    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def get_length(self):
      return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        
    def __add__(self, v):
      return V3(self.x + v.x, self.y + v.y, self.z + v.z)
        
    def __sub__(self, v):
      return V3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, n):
      return V3(self.x * n, self.y * n, self.z * n)
    
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
