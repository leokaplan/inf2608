import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from V3 import V3
import math
from pyquaternion import Quaternion

class Primitive():
    Plane = 1
    Cube = 2
    Sphere = 3

class Transform:
    def RotateAroundAxis(self,axis,vector,degrees):
        return None
    def Rotate(self,quat):
        self.localx = quat.rotate(self.localx)
        self.localy = quat.rotate(self.localy)
        self.localz = quat.rotate(self.localz)
        self.rotation *= quat
        self.rotation_angle = self.rotation.angle
        #print(self.localx)

    def __init__(self,position=None,orientation=None,scale=None):
        self.localx = (1,0,0)
        self.localy = (0,1,0)
        self.localz = (0,0,1)
        self.rotation = Quaternion()
        self.rotation_angle = 0
        if position is None:
            self.position = V3.zero()
        else:
            self.position = position
        if orientation is None:
            self.orientation = V3.zero()
        else:
            self.orientation = orientation
        if scale is None:
            self.scale = V3.one()
        else:
            self.scale = scale


class Object:
    def start(self):
        return None
    
    def update(self,dt):
        return None
    def __init__(self,parent,transform=None):
        if transform == None:
            self.transform = Transform()
            self.gtransform = Transform()
        else:
            self.transform = transform
            self.gtransform = transform
        self.parent = parent
        self.children = []
    def gldraw(self,w,h):
        #glPushMatrix()
        #glRotatef(self.gtransform.rotation.z,*((self.transform.rotation*-1).pure()))
        #glRotatef(self.gtransform.rotation.y,*((self.transform.rotation*-1).pure()))
        #glRotatef(self.gtransform.rotation.x,*((self.transform.rotation*-1).pure()))
        glPushMatrix()
        glTranslatef(*self.transform.position.pure())
        #print(self.transform.rotation.angle)
        #glMultMatrixf(self.transform.rotation.transformation_matrix)
        glRotatef(self.transform.rotation_angle*57.3, *self.transform.localz)
        #glRotatef(120,0,1,1)
        #rotz = (-math.sin(self.transform.rotation.z), math.cos(self.transform.rotation.z), 0)
        #glRotatef(self.transform.rotation.y, *rotz)
        #roty = (self.transform.rotation.y*math.cos(self.transform.rotation.z), self.transform.rotation.y*math.sin(self.transform.rotation.z), 0)
        #glRotatef(self.transform.rotation.x, *roty)
        
        glRotatef(self.transform.rotation_angle*57.3, *self.transform.localy)
        glRotatef(self.transform.rotation_angle*57.3, *self.transform.localx)
        #glRotatef(self.transform.orientation.z,1,1,1)
        #glRotatef(self.transform.orientation.y/57,0,1,0)
        #glRotatef(self.transform.orientation.x/57,1,0,0)
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex].pure())
        glEnd()
        #glPopMatrix()
        glPopMatrix()

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
            [0,2],
            [0,3],
            [5,1],
            [5,7],
            [5,3],
            [6,2],
            [6,7],
            [6,3],
            [4,1],
            [4,7],
            [4,2],
        ]
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
            [0,1],
            [0,2],
            [2,3],
            [1,3],
        ]

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
        self.transform.position -= V3(0,0,5)
        self.speed = V3.zero()

    def update(self,dt):
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
