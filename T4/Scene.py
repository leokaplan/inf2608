from Object import Cube,Camera,Plane,Coord,Object
import pygame



class Scene:
    def __init__(self):
        self.camera = Camera(self)
        self.objects = []
        self.textures = []
        self.indexmap = []
        self.lights = []
        #self.width = width
        #self.height = height
    def createCube(self,transform=None,parent=None):
        if parent is None:
            obj = Cube(self,transform)
            self.objects.append(obj)
        else:
            obj = Cube(parent,transform)
            parent.children.append(obj)

        return obj
    def createPlane(self,transform=None,parent=None):
        obj = Plane(self,transform)
        self.objects.append(obj)
        return obj
    def createCoord(self,transform=None,parent=None):
        obj = Coord(self,transform)
        self.objects.append(obj)
        return obj
    def createEmpty(self,transform=None,parent=None):
        obj = Object(self,transform)
        self.objects.append(obj)
        return obj
    def loadtexture(self,index,path):
        self.presenter.loadtexture(index,path)


