

#from OpenGL.GL import *
#from OpenGL.GLU import *
#from OpenGL.GLUT import *
from glshow import Textureshow,TextureInit
import numpy as np
from V3 import V3,V4
import math

GL_LIGHTING = ""
GL_COLOR_MATERIAL = ""
GL_FRONT_AND_BACK = ""
GL_AMBIENT_AND_DIFFUSE = "" 
GL_AMBIENT,GL_DIFFUSE,GL_POSITION = "","","" 
GL_LIGHT0 = 0
GL_LIGHT1 = 1
GL_TEXTURE_2D = ""
GL_UNPACK_ALIGNMENT = 0
GL_RGB,GL_RGBA = 0,1
GL_UNSIGNED_BYTE = 0
GL_COLOR_BUFFER_BIT,GL_DEPTH_BUFFER_BIT=0,0
GL_DEPTH_TEST = 0
GL_TEXTURE_MAG_FILTER = 0
GL_TEXTURE_MIN_FILTER = 0
GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL=0,0,0
GL_NEAREST = 0
GL_TRIANGLES = 0

def glGenTextures(x):
    return None
def glTexParameterf(x,y,z):
    return None
def glTexEnvf(x,y,z):
    return None
def glBindTexture(x,y):
    return None
def glPixelStorei(x,y):
    return None
def glTexImage2D(x,y,z,w,h,a,c,b,d):
    return None
def glEnable(x):
    return None
def glColorMaterial ( x,y):
    return None
def glLightfv(x,y,z):
    return None

###################################
matrix_stack = []
current = np.identity(4)
current_kind = 0
_w,_h = 0,0
color_buf = []
depth_buf = []

tri = []
_uv = (0,0)
_normal = (0,0,0)

def matrix():
    M = matrix_stack[0] 
    for m in matrix_stack[1:]:
        #print(m)
        M = M@m
    return M

def world2camera(p,M):
    v = np.array([p[0],p[1],p[2],1.])
    v = M@v
    return [
            v[0]/v[3],
            v[1]/v[3],
            v[2]/v[3]
        ]
    
def camera2screen(v):
    global _near
    if v[2] == 0:
        return [_near *v[0],_near*v[1]]
    return [
            _near * v[0] / -v[2], 
            _near * v[1] / -v[2]
        ]

def screen2NDC(v):
    global _w,_h
    b = l = 0
    r = _w
    t = _h
    return [
            (2 * v[0] / (r - l)) - (r + l) / (r - l), 
            (2 * v[1] / (t - b)) - (t + b) / (t - b)
            ]
def NDC2raster(v):
    global _w,_h
    return [
        _w *(1 + v[0]) / 2,
        _h *(1 - v[1]) / 2,
        -v[2]
    ]

def color(i,x,y):
    return (255,0,0)
def edge(a,b,c):
    return (c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])

def contains(t,tri,i,j):
    area = edge(t[0],t[1],t[2])
    a0 =   edge(t[0],t[1],[i,j])
    a1 =   edge(t[1],t[2],[i,j])
    a2 =   edge(t[2],t[0],[i,j])
    uv0 = tri[0][1]
    uv1 = tri[1][1]
    uv2 = tri[2][1]
    if(a0 >= 0 and a1 >= 0 and a2 >= 0):
        a0 /= area
        a1 /= area
        a2 /= area
        c0 = color(0,i,j)
        c1 = color(1,i,j)
        c2 = color(2,i,j)
        r = a0 * c0[0] + a1 * c1[0] + a2 * c2[0]
        g = a0 * c0[1] + a1 * c1[1] + a2 * c2[1] 
        b = a0 * c0[2] + a1 * c1[2] + a2 * c2[2] 
        return True,[r,g,b]
    else:
        return False,None


def clamp(x,a,b):
    if x < a:
        return a
    if x > b:
        return b
    else:
        return x

def renderTri(tri):
    M = matrix()
    #print('####################')
    #print(M)
    ct = []
    bbmin = [np.inf,np.inf]
    bbmax = [-np.inf,-np.inf]
    proj = []
    for v in tri:
        #print(v)
        cam = world2camera(v[0],M)
        #print(cam)
        screen = camera2screen(cam)
        #print(screen)
        pv = screen2NDC(screen)
        #print(pv)
        pv[0] = (pv[0]+1)*_w
        pv[1] = (pv[1]+1)*_h
        if (pv[0] < bbmin[0]): 
            bbmin[0] = pv[0]
        if (pv[1] < bbmin[1]): 
            bbmin[1] = pv[1]
        if (pv[0] > bbmax[0]): 
            bbmax[0] = pv[0]
        if (pv[1] > bbmax[1]): 
            bbmax[1] = pv[1]
        #print(pv)
        proj.append(pv)
    #print()
    # transfer to buffer
    bbmin[0] = int(clamp(bbmin[0],1,_w-1))
    bbmin[1] = int(clamp(bbmin[1],1,_h-1))
    bbmax[0] = int(clamp(bbmax[0],1,_w-1))
    bbmax[1] = int(clamp(bbmax[1],1,_h-1))
    #print(bbmin)
    #print(bbmax)
    #print(bbmin[0],bbmax[0])
    #print(bbmin[1],bbmax[1])
    for i in range(bbmin[0],bbmax[0]):
        for j in range(bbmin[1],bbmax[1]):
            if i == bbmin[0] or i == bbmax[0] or j == bbmin[1] or j == bbmax[1]:
                color_buf[i][j] = [255,255,255]
            boolean,col = contains(proj,tri,i,j)
            if boolean:
                #x,y = int(pv[0]),int(pv[1])
                #print(x,y)
                z = 2#raster2world(i,j)
                if z < depth_buf[i][j]:
                    depth_buf[i][j] = z
                    #print(i,j)
                    color_buf[i][j] = col#color(v,pv[0],pv[1])
            

###################################
GL_MODELVIEW = 0
GL_PROJECTION = 1
def glClear(x):
    global color_buf, depth_buf,_w,_h
    color_buf = np.zeros((_w,_h,3))
    depth_buf = np.full((_w, _h), np.inf)
def glMatrixMode(kind):
    global current_kind
    current_kind = kind
def glLoadIdentity():
    global current
    current = np.identity(4)
def glPushMatrix():
    global matrix_stack
    matrix_stack.append(current)
def glPopMatrix():
    global matrix_stack
    matrix_stack.pop()

        
def glScalef(x,y,z):
    global current
    current = np.identity(4) @ current
        
def glTranslatef(x,y,z):
    global current
    trans = np.identity(4)
    trans[3][0] = x
    trans[3][1] = y
    trans[3][2] = z
    current = trans @ current 
        
def glRotatef(angle, x,y,z):
    global current
    sina = math.sin(angle)
    cosa = math.cos(angle)
    l = np.linalg.norm([x,y,z])
    if l != 0:
        direction = np.array([x,y,z])/l
    else:
        direction = np.array([0,0,0])
    R = np.diag([cosa, cosa, cosa])
    R += np.outer(direction, direction) * (1.0 - cosa)
    direction *= sina
    R += np.array([
        [ 0.0,-direction[2],direction[1]],
        [ direction[2], 0.0,-direction[0]],
        [-direction[1], direction[0],  0.0]
    ])
    M = np.identity(4)
    M[:3, :3] = R
    #print(M)
    current = M @ current 

def glBegin(kind):
    global tri
    tri = []
def glEnd():
    global tri
    renderTri(tri)
def glNormal3dv( n ):
    global _normal
    _normal = n
def glTexCoord2f(u,v):
    global _uv
    _uv = (u,v)
def glVertex3fv(v):
    global tri
    tri.append([v,_uv,_normal])
def gluPerspective(fov, aspect, near, far):
    global _near
    _near = near

######################################
class zbuf:
    def __init__(self,w,h):
        global _w,_h
        _w = w
        _h = h
        TextureInit()
    def createLight(self,index,pos,color,ambient_color):
        glEnable ( GL_LIGHTING ) 
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
        if index == 0:
            light = GL_LIGHT0
        if index == 1:
            light = GL_LIGHT1
        glEnable(light) 
        glLightfv(light, GL_AMBIENT, ambient_color.pure());
        glLightfv(light, GL_DIFFUSE, color.pure());
        #glLightfv(light, GL_SPECULAR, light_specular);
        glLightfv(light, GL_POSITION, pos.pure());

    def loadtexture(self,index,img):
        glEnable(GL_TEXTURE_2D)
        index = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, index)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img['w'], img['h'],0, GL_RGBA, GL_UNSIGNED_BYTE, img['data'])
        return index

    def init(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        ###############
        TextureInit()

    def draw(self,scene,cb):
        self.rendercamera(scene.camera)
        for o in scene.objects:
            self.render(o,scene.indexmap)
        #########################
        global color_buf
        Textureshow(color_buf,scene.w,scene.h)
        cb()

    def selecttex(self,index):
        
        glEnable(GL_TEXTURE_2D) 
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
        glBindTexture(GL_TEXTURE_2D, index)

    def render(self,obj,indexmap):
        glPushMatrix()

        
        glScalef(*obj.transform.scale.pure())
        
        glTranslatef(*obj.transform.position.pure())
        
        glRotatef(obj.transform.rotation.z, 0,0,1)
        glRotatef(obj.transform.rotation.y, 0,1,0)
        glRotatef(obj.transform.rotation.x, 1,0,0)
        
        
        
        for child in obj.children:
            self.render(child,indexmap)
        
        for face in obj.faces:
            facei = obj.faces.index(face)
            self.selecttex(indexmap[obj.textures[facei]])
            glBegin(GL_TRIANGLES)
            vcount = 0
            for edge in face[0]:
                vertex = obj.edges[edge][0]
                v = obj.vertices[vertex].pure()
                uv = face[1]
                glNormal3dv( face[2] )
                glTexCoord2f(uv[vcount][0],uv[vcount][1])
                glVertex3fv(v)
                vcount += 1
            glEnd()
        glPopMatrix()


    def rendercamera(self,camera):
        gluPerspective(camera.fov, float(camera.parent.w/camera.parent.h), camera.near, camera.far)
        glTranslatef(*(camera.transform.position).pure())
