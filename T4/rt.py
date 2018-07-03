import numpy as np
class RGBImage(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = np.zeros((self.height, self.width, 3), dtype=np.uint8)
    def drawPixel(self, x, y, r, g, b):
        self.data[y][x][0] = r
        self.data[y][x][1] = g
        self.data[y][x][2] = b



def raytrace(scene):
    image = RGBImage(scene.w,scene.h)
    for x in range(0,scene.w):
        for y in range(0,scene.h):
            image.drawPixel(x, y, r, g, b)
    print('done')
    return image

