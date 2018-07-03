
import pygame
from pygame.locals import *

#from pylab import *
from numpy import *
from time import clock
from rt import raytrace
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
        pygame.key.set_repeat(10,10)
        self.backend = gl()

    def show(self,scene):
        scene.w = self.w
        scene.h = self.h
        scene.camera.start()
        for o in scene.objects:
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
            scene.camera.update(self.dt)
            for o in scene.objects:
                o.update(self.dt)
            self.backend.draw(scene)
            pygame.display.flip()
            pygame.time.wait(1)
    
    def rcshow(self,scene):
        scene.w = self.w
        scene.h = self.h
        img = raytrace(scene)
        #OpenGL init
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0,self.w,0,self.h,-1,1)
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_DEPTH_TEST)
        glClearColor(0.0,0.0,0.0,0.0)
        glEnable(GL_TEXTURE_2D)

        #Set texture
        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.w, self.h, 0, GL_RGB, GL_UNSIGNED_BYTE, img.data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glActiveTexture(GL_TEXTURE0)

        #Clean start
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        #draw rectangle
        #glTranslatef(300,200,0)
        glBegin(GL_QUADS)
        glTexCoord(0,0)
        glVertex2f(0,0)

        glTexCoord(0,1)
        glVertex2f(0,self.h)

        glTexCoord(1,1)
        glVertex2f(self.w,self.h)

        glTexCoord(1,0)
        glVertex2f(self.w,0)
        
        glEnd()

        glFlush()
        pygame.display.flip()
        print('done 2')
        #game loop until exit
        gameExit = False
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

