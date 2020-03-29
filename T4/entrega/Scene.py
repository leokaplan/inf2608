from Object import Transform,Cube,Camera,Plane,Coord,Object,Light
import pygame



class Scene:
    def __init__(self):
        self.camera = Camera(self)
        self.objects = []
        self.textures = []
        self.indexmap = []
        self.lights = []
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
    def createLight(self,pos,color,ambient_color):
        light = Light(self,Transform(pos.HV3()),color,ambient_color)
        self.lights.append(light)
        self.presenter.createLight(
                len(self.lights)-1,
                light.transform.position,
                color,
                ambient_color
        )

    def loadtexture(self,index,path):
        self.presenter.loadtexture(index,path)


