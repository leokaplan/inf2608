
import pygame
from pygame.locals import *
from Scene import Scene
from Presenter import Presenter
from Object import Transform
from V3 import V3
import types
import math
from pyquaternion import Quaternion

scene = Scene()
rot0 = V3(-1/1.4,1/1.4,0)*54.7
rot0 = V3(-54.7/1.4,54.7/1.4,54.7/1.4)
mar = math.atan(1/math.sqrt(2))
ma = math.degrees(mar)
#ma = math.atan(1/math.sqrt(2))
#rot0 = V3(ma,ma,ma)
#rot0 = V3(30,30,0)
rot0 = Quaternion(axis=[1, 1, 1], angle=3.142)
rot1 = Quaternion(axis=[1, 1, 1], angle=2*3.14159265/3)
rot_0 = Quaternion(axis=[1, 1, 1], angle=0)
rot_1 = Quaternion(axis=[1, 0, 1], angle=3.14/2)
rot_2 = Quaternion(axis=[0, 1, 1], angle=mar)
rot_3 = Quaternion(axis=[1, 1, 0], angle=mar/3.14)
print(rot1)
rot = rot_0*rot_1*rot_2*rot_3
#rot1*rot0#*rot1.inverse
print(rot)
res = rot1.rotate([1,1,0])
res = V3(0,54.7,54.7)
xq = rot1.rotate((1,0,0))
yq = rot1.rotate((0,1,0))
zq = rot1.rotate((0,0,1))
#print(*rot.axis)
#rote = V3(*res)*57.2958
#print(rote.pure())
#rot0 = V3(0,45,51.9615)
#print('b')
#print(rot1)
#print('a')
#V3(34,50,45))
cube = scene.createCube(Transform(V3(0,(3**(1/2)/2),0)))
cube.transform.Rotate(rot)
cube.i = 0
def rotate(self,dt):
    rot_ = Quaternion(axis=[1, 0, 0], angle=self.i)
    #self.transform.Rotate(rot_)
    #self.transform.rotation = rot_
    self.i+=0.01
    #self.transform.rotation.y += 10*dt*math.sin(self.transform.rotation.z)
    #self.transform.rotation.x -= 10*dt*math.sin(self.transform.rotation.z)
    #self.transform.RotateAroundAxis((V3.right(),V3.up(),V3.front()),V3.up(),1)
    #self.transform.rotation.y += 1
    #self.transform.rotation.z += 1
    spd = 10
    pressed = pygame.key.get_pressed()
    
    #self.gtransform.rotation.y += spd*dt
    #self.transform.rotation.x += 10
    #self.transform.rotation.z += 10
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
    #self.transform.rotation.z -= 10*dt
    #self.transform.rotation.x += math.cos(10*dt)
cube.update = types.MethodType(rotate,cube)
#scene.createPlane(Transform(V3(1,1,0),None))
scene.createCoord()
presenter = Presenter(400,300)
presenter.show(scene)

