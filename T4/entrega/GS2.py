import pygame
from Scene import Scene
from Presenter import Presenter
from Object import Transform
from V3 import V3,V4
import types
import math
from Material import Material

scene = Scene()


def startCam(self):
    self.fov = 90
    self.near = 1
    self.far = 50
    self.transform.position = V3(0.,0,-1.)
    self.speed = V3.zero()
    self.LookAt = V3.zero()


presenter = Presenter(400,300)
presenter.bind(scene)

scene.loadtexture(0,'t4puc-rio.jpeg')
scene.createLight(
        V4(5.,5.,0.,1.),
        V4(0.7,0.7,0.5,1.0),
        V4(0.5,0.5,0.5,1.0)
)

plane = scene.createPlane()
plane.transform.position = V3(0,0,0)
#plane.material = Material(1,1,1)
plane.textures = [0,0]
plane.material = Material(1,0.0,0.0)
plane.i = 0.2
def updatep(self,dt):
    self.faces[0][2] = [0,math.sin(self.i),0]
    self.i += 0.2


plane.update = types.MethodType(updatep,plane)
scene.camera.start = types.MethodType(startCam,scene.camera)

presenter.show()
