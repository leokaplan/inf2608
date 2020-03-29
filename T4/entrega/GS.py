import pygame
from Scene import Scene
from Presenter import Presenter
from Object import Transform
from V3 import V3,V4
import types
import math
from Material import Material

scene = Scene()


def rotate(self,dt):
    self.transform.rotation.y += 30*dt
    for child in self.children:
        child.update(dt) 

def rotateK(self,dt):
    spd = 10
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_a]:
        self.transform.rotation.x += spd*dt
    if pressed[pygame.K_d]:
        self.transform.rotation.x -= spd*dt
    if pressed[pygame.K_s]:
        self.transform.rotation.y += spd*dt
    if pressed[pygame.K_w]:
        self.transform.rotation.y -= spd*dt
    if pressed[pygame.K_q]:
        self.transform.rotation.z += spd*dt
    if pressed[pygame.K_e]:
        self.transform.rotation.z -= spd*dt
    if pressed[pygame.K_SPACE]:
        self.transform.rotation.x = 0
        self.transform.rotation.y = 0
        self.transform.rotation.z = 0
    if pressed[pygame.K_z]:
        print(self.transform.rotation.pure())

def startCam(self):
    self.fov = 90
    self.near = 1
    self.far = 50
    self.transform.position -= V3(0,1,3)
    self.speed = V3.zero()
    self.LookAt = V3.zero()

def updateCam(self,dt):
        self.speed = V3.zero()
        spd = 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.speed += V3(1,0,0)*-spd
                if event.key == pygame.K_RIGHT:
                    self.speed += V3(1,0,0)*spd
                if event.key == pygame.K_DOWN:
                    self.speed += V3(0,1,0)*-spd
                if event.key == pygame.K_UP:
                    self.speed += V3(0,1,0)*spd
        self.transform.position -= self.speed*dt
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    self.speed = V3.zero()





textures = ['t4puc-rio.jpeg','t4bufalo.jpeg','t4chita.jpeg','t4danna.jpeg','t4elefante.jpeg','t4girafa.jpeg','t4rino.jpeg']

presenter = Presenter(400,300)
presenter.bind(scene)

scene.createLight(
        V4(2.5,0,1.5,1),
        V4(0.8,0.8,0.8,1.0),
        V4(0.1,0.1,0.1,1.0)
)
scene.createLight(
        V4(0,0,4,1),
        V4(0.7,0.7,0.7,1.0),
        V4(0.1,0.1,0.1,1.0)
)
for t in textures:
    scene.loadtexture(textures.index(t),t)

plane = scene.createPlane()
plane.transform.rotation.x = 90
plane.transform.scale.x = 2
plane.transform.scale.z = 2
plane.textures = [0,0]
plane.material = Material(0.75,0.5,0.25)

empty = scene.createEmpty()
empty.update = types.MethodType(rotate,empty)

cube = scene.createCube(Transform(V3(0,(3**(1/2)/2),0),V3(-79,-42,44.5)),empty)
cube.textures = [1,1,2,2,3,3,4,4,5,5,6,6]
cube.update = types.MethodType(rotateK,cube)
#cube.material = Material(V3(1,0,0),V3(1,1,1))
cube.material = Material(1,1,1)

scene.camera.update = types.MethodType(updateCam,scene.camera)
scene.camera.start = types.MethodType(startCam,scene.camera)

presenter.show()
