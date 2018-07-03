from Object import Cube,Camera,Plane,Coord



class Scene:
    def __init__(self):
        self.camera = Camera(self)
        self.objects = []
        self.lights = []
        #self.width = width
        #self.height = height
    def createCube(self,transform=None,parent=None):
        obj = Cube(self,transform)
        self.objects.append(obj)
        return obj
    def createPlane(self,transform=None,parent=None):
        obj = Plane(self,transform)
        self.objects.append(obj)
        return obj
    def createCoord(self,transform=None,parent=None):
        obj = Coord(self,transform)
        self.objects.append(obj)
        return obj
