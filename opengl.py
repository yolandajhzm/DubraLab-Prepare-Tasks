import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
class DrawShape(object):
    def __init__(self):
        # init glut (fixed steps)
        glutInit()  
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA) 
        glutInitWindowSize(400, 400)
        glutCreateWindow("Hello OpenGL")  

        self.setup()

        glutDisplayFunc(self.draw_rectangle) 
        # glutDisplayFunc(self.draw_line) 

        # glutSwapBuffers()
        glutMainLoop()

    def setup(self):
       glClearColor(1.0, 1.0, 1.0, 1.0) # set background color to white
    #    gluOrtho2D(-8.0, 8.0, -8.0, 8.0)

    def draw_line(self):
        # fixed start
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(1.0, 0.0, 0.0)  # set color to red
        glBegin(GL_LINES)
        glVertex2f(.25, .25)
        glVertex2f(.75, .75)
        glEnd()
        glFlush()  # draw

        # fixed end
        glutSwapBuffers() 
    
    def draw_rectangle(self):
        # fixed start
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(1.0, 0.0, 0.0)  # set color to red
        # customized positions
        glBegin(GL_QUADS)
        glVertex2f(-0.2, .2)
        glVertex2f(-0.2, .5)
        glVertex2f(-0.5, .5)
        glVertex2f(-0.5, .2)
        glEnd()

        # glRectf(-0.75,0.75, 0.75, -0.75)
        glFlush()  # draw

        # fixed end
        glutSwapBuffers() #？When rendering graphics, you need to exchange buffers, the front buffer is used for rendering, the latter is used for calculation, double buffering

if __name__ == "__main__":
    DrawShape()

# QUESTION: how to draw both shapes in one window, with different methods?