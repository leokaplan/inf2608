
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class gl:
    def init(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def draw(self,scene):
        self.rendercamera(scene.camera)
        for o in scene.objects:
            self.render(o)
    def render(self,obj):
        glPushMatrix()
        glTranslatef(*obj.transform.position.pure())
        glRotatef(obj.transform.rotation_angle*57.3, *obj.transform.localz)
        glRotatef(obj.transform.rotation_angle*57.3, *obj.transform.localy)
        glRotatef(obj.transform.rotation_angle*57.3, *obj.transform.localx)
        glBegin(GL_LINES)
        for edge in obj.edges:
            for vertex in edge:
                glVertex3fv(obj.vertices[vertex].pure())
        glEnd()
        glPopMatrix()
    def rendercamera(self,camera):
        gluPerspective(60, (camera.parent.w/camera.parent.h), 0.1, 50.0)
        glTranslatef(*(camera.transform.position).pure())
