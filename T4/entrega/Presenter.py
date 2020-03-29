import pygame
from pygame.locals import *

from numpy import *
from time import clock

from rc import rc
from zbuf import zbuf
from gl import gl

class Presenter:
    def __init__(self,w,h):
        self.w,self.h = w,h
        pygame.init()
        display = (self.w,self.h)
        self.screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        self.dto = 0
        self.t = 0
        self.clock = pygame.time.Clock()
        pygame.mixer.pause()
        pygame.key.set_repeat(10,10)
        self.backend = rc(w,h)
        #self.backend = gl(w,h)
        #self.backend = zbuf(w,h)
    def bind(self,scene):
        self.scene = scene
        scene.presenter = self
    
    def createLight(self,i,pos,color,ambient_color):
        self.backend.createLight(i,pos,color,ambient_color)
    def loadtexture(self,index,path):
        textureSurface = pygame.image.load(path)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        self.scene.textures.insert(index, {'data':textureData,'w':width,'h':height})
        newindex = self.backend.loadtexture(index,self.scene.textures[index])
        self.scene.indexmap.insert(index,newindex)


    def show(self):
        self.scene.w = self.w
        self.scene.h = self.h
        self.scene.camera.start()
        for o in self.scene.objects:
            o.start()
        while True:
            self.clock.tick()
            print('FPS [%f] \r'%self.clock.get_fps(),end="")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.backend.init()
            self.t = pygame.time.get_ticks()
            self.dt = (self.t - self.dto) / 1000.0
            self.dto = self.t
            self.scene.camera.update(self.dt)
            for o in self.scene.objects:
                o.update(self.dt)
            self.backend.draw(self.scene,pygame.display.flip)
            pygame.time.wait(1)
    
