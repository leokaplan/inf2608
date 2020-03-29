from V3 import V3,V4
import math
import numpy as np

def edge(a,b,c):
    return (c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])

class Transform:
    def __init__(self,position=None,rotation=None,scale=None):
        self.localx = (1,0,0)
        self.localy = (0,1,0)
        self.localz = (0,0,1)
        if position is None:
            self.position = V3.zero()
        else:
            self.position = position
        if rotation is None:
            self.rotation = V3.zero()
        else:
            self.rotation = rotation
        if scale is None:
            self.scale = V3.one()
        else:
            self.scale = scale


class Object:
    def start(self):
        return None
    
    def intersect(self,orig,dest):
        return np.inf
        return NotImplemented
    
    def normal(self,intersect):
        return V3(0,0,0)
        return NotImplemented
    
    def update(self,dt):
        for child in self.children:
            child.update(dt) 
        return None
    def __init__(self,parent,transform=None):
        if transform == None:
            self.transform = Transform()
            self.gtransform = Transform()
        else:
            self.transform = transform
            self.gtransform = transform
        self.faces = []
        self.parent = parent
        self.children = []

class Cube(Object):
    def __init__(self,parent,transform):
        super().__init__(parent,transform)
        self.vertices = [
            V3(-0.5,-0.5,-0.5),
            V3(0.5,-0.5,-0.5),
            V3(-0.5,0.5,-0.5),
            V3(-0.5,-0.5,0.5),
            V3(0.5,0.5,-0.5),
            V3(0.5,-0.5,0.5),
            V3(-0.5,0.5,0.5),
            V3(0.5,0.5,0.5)
        ]
        self.edges = [
            [0,1],
            [1,5],
            [5,0],
            
            [0,5],
            [5,3],
            [3,0],

            [2,4],
            [4,1],
            [1,2],
            
            [2,1],
            [1,0],
            [0,2],

            [4,7],
            [7,5],
            [5,4],
            
            [4,5],
            [5,1],
            [1,4],

            
            [7,6],
            [6,3],
            [3,7],
            
            [7,3],
            [3,5],
            [5,7],

            
            [6,2],
            [2,0],
            [0,6],
            
            [6,0],
            [0,3],
            [3,6],
            
            [6,7],
            [7,4],
            [4,6],

            [6,4],
            [4,2],
            [2,6],
        ]
        self.faces = [
            [[0,1,2],   [(0,1),(1,1),(1,0)],[0,-1,0]],
            [[3,4,5],   [(0,1),(1,0),(0,0)],[0,-1,0]],
            [[6,7,8],   [(0,1),(1,1),(1,0)],[0,0,-1]],
            [[9,10,11], [(0,1),(1,0),(0,0)],[0,0,-1]],
            [[12,13,14],[(0,1),(1,1),(1,0)],[+1,0,0]],
            [[15,16,17],[(0,1),(1,0),(0,0)],[+1,0,0]],
            [[18,19,20],[(0,1),(1,1),(1,0)],[0,0,+1]],
            [[21,22,23],[(0,1),(1,0),(0,0)],[0,0,+1]],
            [[24,25,26],[(0,1),(1,1),(1,0)],[-1,0,0]],
            [[27,28,29],[(0,1),(1,0),(0,0)],[-1,0,0]],
            [[30,31,32],[(0,1),(1,1),(1,0)],[0,+1,0]],
            [[33,34,35],[(0,1),(1,0),(0,0)],[0,+1,0]],
        ]
    def intersect(self,orig,dest):
        return 0
    def normal(self,intersect):
        return  V3(0,0,1)

class Plane(Object):
    def __init__(self,parent,transform):
        super().__init__(parent,transform)
        self.vertices = [
            V3(-0.5,-0.5,0),
            V3(0.5,-0.5,0),
            V3(-0.5,0.5,0),
            V3(0.5,0.5,0)
        ]
        self.edges = [
            [2,3],
            [3,1],
            [1,2],
            
            [2,1],
            [1,0],
            [0,2]
        ]
        self.faces = [
            [[0,1,2],[(0,1),(1,1),(1,0)],[0,0,1]],
            [[3,4,5],[(0,1),(1,0),(0,0)],[0,0,1]]
        ]
    def intersect(self,orig,dest):
        normal = V3(*self.faces[0][2])
        orig = orig.normalize()
        dest = orig.normalize()
        denom = V3.dot(normal,dest)
        if denom < 1e-6:
            return np.inf
        d = V3.dot(self.transform.position - orig, normal) / denom
        if d < 0:
            return np.inf
        return d
    def normal(self,intersect):
        return  V3(*self.faces[0][2])


class Coord(Object):
    def __init__(self,parent,transform):
        super().__init__(parent,transform)
        size = 5
        self.vertices = [
            V3(0,0,0)*size,
            V3(1,0,0)*size,
            V3(0,1,0)*size,
            V3(0,0,1)*size
        ]
        self.edges = [
            [0,1],
            [0,2],
            [0,3]
        ]

class Camera(Object):
    def start(self):
        return None
    def update(self,dt):
        return None

class Light(Object):
    def __init__(self,parent,transform,color,ambient_color):
        super().__init__(parent,transform)
        self.color = color
        self.ambient = ambient_color
        self.Kspecular = 1.

