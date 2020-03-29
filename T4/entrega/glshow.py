
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
def TextureInit():
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

def Textureshow(img,w,h):
    img = pygame.surfarray.make_surface(img)
    img = pygame.image.tostring(img, "RGBA",True)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,w,0,h,-1,1)
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_DEPTH_TEST)
    glClearColor(0.0,0.0,1.0,0.0)
    glEnable(GL_TEXTURE_2D)

    #glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    #glPixelStorei(GL_PACK_SKIP_ROWS, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    #glGenerateMipmap(GL_TEXTURE_2D)

    glActiveTexture(GL_TEXTURE0)

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    #glTranslatef(300,200,0)
    glBegin(GL_QUADS)
    glTexCoord(0,0)
    glVertex2f(0,0)

    glTexCoord(0,1)
    glVertex2f(0,h)

    glTexCoord(1,1)
    glVertex2f(w,h)

    glTexCoord(1,0)
    glVertex2f(w,0)
    
    glEnd()

    glFlush()


