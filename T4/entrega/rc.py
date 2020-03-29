from V3 import V3,V4
import numpy as np
from glshow import Textureshow,TextureInit
import matplotlib.pyplot as plt
import math
class RGBImage(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = np.zeros((self.width, self.height, 3))#, dtype=np.uint8)

    def drawPixel(self, x, y, r, g, b):
        self.data[y][x][0] = r
        self.data[y][x][1] = g
        self.data[y][x][2] = b

def TriIntersect(tri,o,dest):
    v0 = tri[0]
    v1 = tri[1]
    v2 = tri[2]
    v0v1 = v1 - v0
    v0v2 = v2 - v0
    N = v0v1.cross(v0v2)
    area = N.len()
    NR = V3.dot(N,dest)
    if math.fabs(NR) < 1e-6:
        return np.inf

    d = V3.dot(N,v0)

    t = (V3.dot(N,o) + d) / NR
    
    #if t < 0:
    #    return np.inf
    
    P = o + t * dest
    edge0 = v1 - v0
    vp0 = P - v0
    C = edge0.cross(vp0);
    if V3.dot(N,C) < 0:
        return np.inf,N
    
    edge1 = v2 - v1
    vp1 = P - v1
    C = edge0.cross(vp1);
    if V3.dot(N,C) < 0:
        return np.inf,N

    edge2 = v0 - v2
    vp2 = P - v2
    C = edge0.cross(vp2);
    if V3.dot(N,C) < 0:
        return np.inf,N

    return d,N



class rc:
    def __init__(self,w,h):
        self.image = RGBImage(w,h)
        TextureInit()
        self.num_bounces = 1

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
    def trace_ray(self,rayO, rayD,scene):
        # traca o raio 
        dist_min = np.inf
        N = [0,0,0]
        for obj in scene.objects:
	    #for face in obj.faces:
	    #vs = []
	    #for f in face[0]:
	    #e = obj.edges[f]
	    #v = obj.vertices[e[0]]
	    #vs += [v]
	    #dist_obj,n = TriIntersect(vs,rayO, rayD)
            dist_obj = obj.intersect(rayO, rayD)
            if dist_obj < dist_min:
                dist_min = dist_obj
                i_min = scene.objects.index(obj)
	    #N = n
        # Raio nao interceptou nada, sai
        if dist_min == np.inf:
            return
        # Senao, ele bateu em algo (vamos pegar o mais proximo)
        obj = scene.objects[i_min]
        # andamos dist_min na direcao destino saindo da origem 
        # p achar o ponto de intersecao
        M = rayO + rayD * dist_min
        
        N = obj.normal(M)
        toL = (scene.lights[0].transform.position - M).normalize()
        toO = (scene.camera.transform.position - M).normalize()
        # Sombras
        l = [obj_sh.intersect(M + N * .0001, toL) for k, obj_sh in enumerate(scene.objects) if k != i_min]
        if l and min(l) < np.inf:
            return
        #Cores
        obj_color = V4.one()
        col_ray = scene.lights[0].ambient
        #print(col_ray.pure())
        # Lambert shading (diffuse)
        #print(V3.dot(N, toL)) 
        col_ray += obj.material.diffuse * max(V3.dot(N, toL),0) * obj_color

        #print(col_ray.pure())
        # Blinn-Phong shading (specular)
        col_ray += obj.material.specular * max(V3.dot(N, (toL + toO).normalize()),0) ** scene.lights[0].Kspecular * scene.lights[0].color
        #print(col_ray.pure())
        return obj, M, N, col_ray


    def trace(self,x,y,scene):
        O = scene.camera.transform.position
        Q = scene.camera.LookAt
        color = V3.zero()
        Q.x = x
        Q.y = y
        #converter Q para coordenada de mundo?
        D = (Q - O).normalize()
        rayO = O
        rayD = D
        reflection = 1.
        bounce = 0
        while bounce < self.num_bounces:
            hit = self.trace_ray(rayO, rayD,scene)
            if hit is None:
                break
            obj, M, N, col_ray = hit
            # reflexao
            rayO = M + N * .0001
            rayD = (rayD - 2 * V3.dot(rayD, N) * N).normalize()
            bounce += 1
            color += reflection * col_ray
            if hasattr(obj,'material'):
                reflection *= obj.material.reflection
        return color
    def draw(self,scene,cb):
        scale = math.tan(math.radians(scene.camera.fov * 0.5))
        r = float(scene.w) / float(scene.h)
        # tela em espaco de pixels (NDC)
        #S = (-1., -1. / r + .25, 1., 1. / r + .25)
        S = (-1., -1. , 1., 1.)
        #S = (0., 0., 1., 1. )
        for i,x in enumerate(np.linspace(S[0], S[2], scene.w)):
            for j, y in enumerate(np.linspace(S[1], S[3], scene.h)):

                #a,b = (2*(i+0.5)/scene.w-1) * r * scale, (1-2*(j+0.5)/scene.h)*scale
                a,b = i,j
                color = self.trace(a,b,scene) 
                color = color.clamp(0,1)
                color *= 255.
                a,b = int(x*scene.w), int(y*scene.h)
                if a < scene.w and b < scene.h:
                    #self.image.drawPixel(a,b, color.x, color.y, color.z)
                    self.image.data[i,scene.h - j - 1, :] = color.pure()

            Textureshow(self.image.data,scene.w,scene.h)
            cb()
            #print('row')
        #print('done')
        #plt.imsave('fig2.png', img)
        print('done2')
        #Textureshow(self.image.data,scene.w,scene.h)
