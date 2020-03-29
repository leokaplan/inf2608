
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
    self.transform.position -= V3(0,0,3)
    self.speed = V3.zero()
    self.LookAt = V3.zero()

textures = ['t4puc-rio.jpeg','t4bufalo.jpeg','t4chita.jpeg','t4danna.jpeg','t4elefante.jpeg','t4girafa.jpeg','t4rino.jpeg']
presenter = Presenter(400,300)
presenter.bind(scene)
scene.loadtexture(0,textures[0])

scene.createLight(
        V4(0,0,4,1),
        V4(0.7,0.7,0.7,1.0),
        V4(0.1,0.1,0.1,1.0)
)
plane = scene.createPlane()

#plane.transform.rotation.x = 90
plane.textures = [0,0]
plane.material = Material(0.75,0.5,0.25)

scene.camera.start = types.MethodType(startCam,scene.camera)

presenter.show()
