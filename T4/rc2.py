from PIL import Image
from io import BytesIO
import pygame
from V3 import V3,V4
import numpy as np
from glshow import Textureshow,TextureInit
import matplotlib.pyplot as plt
class RGBImage(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = np.zeros((self.height, self.width, 3))#, dtype=np.uint8)

    def drawPixel(self, x, y, r, g, b):
        self.data[y][x][0] = r
        self.data[y][x][1] = g
        self.data[y][x][2] = b
class rc2:
    def __init__(self,w,h):
        self.image = RGBImage(w,h)
        TextureInit()

    def rendercamera(self,camera):
        return None
    def init(self):
        return None
    def createLight(self,index,pos,color,ambient_color):
        return None
    def loadtexture(self,index,img):
        return None
    def selecttex(self,index):
        return None
    def draw(self,scene):
        for x in range(0,scene.w):
            for y in range(0,scene.h):
                self.image.drawPixel(x, y, 255.*x/scene.w, 0., 255.*y/scene.h)
        print()
        Textureshow(img,scene.w,scene.h)
