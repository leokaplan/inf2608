
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class gl:
    def __init__(self,w,h):
        glEnable ( GL_LIGHTING ) 
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D) 
    def createLight(self,index,pos,color,ambient_color):
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
        index = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, index)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img['w'], img['h'],0, GL_RGBA, GL_UNSIGNED_BYTE, img['data'])
        return index

    def init(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def draw(self,scene,cb):
        self.rendercamera(scene.camera)
        for o in scene.objects:
            self.render(o,scene.indexmap)
        cb()
    def selecttex(self,index):
        
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
