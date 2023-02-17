from OpenGL.GL import *
import wx
from wx import glcanvas
from OpenGL.GL import *
import cv2
from OpenGL.GL import *
import numpy as np 
import shader as shader
import os
import sys

# cite: https://nicolbolas.github.io/oldtut/Basics/Tut01%20Dissecting%20Display.html

class OpenGLCanvas(wx.glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(680, 630))
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        glClearColor(0.1, 0.15, 0.1, 0.3)
        self.Bind(wx.EVT_PAINT, self.OnDraw)

        os.environ['PYOPENGL_PLATFORM'] = 'egl'

        im0 = cv2.imread("cat_noise.png")
        im1 = cv2.imread("noise.png")

        height, width, _ = im0.shape

        ###### set up VAO and VBO ########
        """
        1. vertices array: position, color, texture
        2. generate VAO and VBO
        3. bind VAO 
        4. bind VBO and allocate memory
        5. set vertex attribute pointer -> corresponds to the layout in the shader
        6. import shader
        """
        self.vertices = np.array([0.5, 0.5, 0,    1.0, 1.0,   # right-up
                                  0.5,-0.5, 0,    1.0, 0.0,   # right-bottom
                                  -0.5, 0.5, 0,   0.0, 1.0,   # left-up
                                  0.5,-0.5, 0,    1.0, 0.0,   # right-bottom
                                  -0.5,-0.5, 0,   0.0, 0.0,  # left-bottom
                                  -0.5, 0.5, 0,   0.0, 1.0], dtype = np.float32)  # left-up      

        VAO = glGenVertexArrays(1) # bundle associated data with a vertex array 
        VBO = glGenBuffers(1) # creating a buffer object to store our data
        glBindVertexArray(VAO) # creates the object / makes it active

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(self.vertices), self.vertices, GL_STATIC_DRAW) # allocate sufficient memory on the CPU

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0)) # stride = 4 x 5
        glEnableVertexAttribArray(0) # position attribute
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12)) # offset = 4 x 3
        glEnableVertexAttribArray(1) # texture attribute

        self.shaderProgram = shader.Shader("./img.vs.glsl", "./img.fsv2.glsl")
        self.VAO = VAO
        self.VBO = VBO

        ###### set up texture ########
        """
        1. generate texture
        2. bind texture
        3. set texture parameters -> (wrap and filter)
        """

        self.texture1 = glGenTextures(1) # generate one texture object
        glBindTexture(GL_TEXTURE_2D, self.texture1) # can remove this line? 
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, im0)

        self.texture2 = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture2) # can remove this line? 
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, im1)

    def OnDraw(self, event):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
    
        self.shaderProgram.use()
        
        ###### set up texture ########
        """
        1. activate texture unit
        2. bind texture
        3. set texture uniform
        """

        glActiveTexture(GL_TEXTURE0) # activate texture unit 0
        glBindTexture(GL_TEXTURE_2D, self.texture1) # store texture 0 in texture1 buffer
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture2)

        glUniform1i(glGetUniformLocation(self.shaderProgram.shaderProgram, "texture1"), 0) # set the texture1 to texture unit 0
        glUniform1i(glGetUniformLocation(self.shaderProgram.shaderProgram, "texture2"), 1)
        
        glDrawArrays(GL_TRIANGLES, 0, 6) # draw two triangles, 3 vertices each
        glFlush()


        self.SwapBuffers()
        

class Window(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, parent=None, title=title, size=(1280, 720))
        self.canvas = OpenGLCanvas(self)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = Window("Hello World!")
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop() # infinitely display the window