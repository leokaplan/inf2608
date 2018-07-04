
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class gl:
    def loadtexture(self,index,img):
        glEnable(GL_TEXTURE_2D)
        glGenTextures(1)
        index = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, index)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img['w'], img['h'],0, GL_RGBA, GL_UNSIGNED_BYTE, img['data'])
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        return index

    def init(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def draw(self,scene):
        self.rendercamera(scene.camera)
        for o in scene.objects:
            self.render(o,scene.indexmap)
    def selecttex(self,index):
        
        glEnable(GL_TEXTURE_2D)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
        glBindTexture(GL_TEXTURE_2D, index)

    def render(self,obj,indexmap):
        glPushMatrix()

        glTranslatef(*obj.transform.position.pure())
        
        #glRotatef(obj.transform.rotation_angle*57.3, *obj.transform.localz)
        #glRotatef(obj.transform.rotation_angle*57.3, *obj.transform.localy)
        #glRotatef(obj.transform.rotation_angle*57.3, *obj.transform.localx)
        glRotatef(obj.transform.rotation.z, 0,0,1)
        glRotatef(obj.transform.rotation.y, 0,1,0)
        glRotatef(obj.transform.rotation.x, 1,0,0)
        
        for child in obj.children:
            self.render(child,indexmap)
        
        for face in obj.faces:
            facei = obj.faces.index(face)
            self.selecttex(indexmap[obj.textures[facei]])
            glBegin(GL_TRIANGLES)
            #glBegin(GL_LINES)
            #for uv in obj.uv[facei]:
            vcount = 0
            for edge in face[0]:
                vertex = obj.edges[edge][0]
                #for vertex in obj.edges[edge]:
                v = obj.vertices[vertex].pure()
                uv = face[1]
                #vi = obj.edges[edge].index(vertex)
                glTexCoord2f(uv[vcount][0],uv[vcount][1])
                #print(uv[vi][0],uv[vi][1])
                #print(vertex)
                glVertex3fv(v)
                vcount += 1
            glEnd()
        '''
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0,  1.0, -1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1.0, -1.0,  1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glEnd()
        '''
        glPopMatrix()

    def rendercamera(self,camera):
        gluPerspective(60, (camera.parent.w/camera.parent.h), 0.1, 50.0)
        glTranslatef(*(camera.transform.position).pure())
