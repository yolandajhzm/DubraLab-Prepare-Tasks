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
 
class Shader:
    def __init__(self, vertex_path, fragment_path):
        with open(vertex_path, mode='r', encoding='utf-8') as vertex_stream:
            vertex_code = vertex_stream.readlines()
        with open (fragment_path, mode='r', encoding='utf-8') as fragment_stream:
            fragment_code = fragment_stream.readlines()
 
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_code)
        glCompileShader(vertex_shader)
        status = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if not status:
            print("[ERROR]: " + bytes.decode(glGetShaderInfoLog(vertex_shader)))
 
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_code)
        glCompileShader(fragment_shader)
        status = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
        if not status:
            print("[ERROR]: " + bytes.decode(glGetShaderInfoLog(fragment_shader)))
 
        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)
        status = glGetProgramiv(shader_program, GL_LINK_STATUS )
        if not status:
            print("[ERROR]: " + bytes.decode(glGetProgramInfoLog(shader_program)))
 
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        self.shaderProgram = shader_program

    def use(self):
        glUseProgram(self.shaderProgram)
 
    def delete(self):
        glDeleteProgram(self.shaderProgram)

class OpenGLCanvas(wx.glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(680, 630))
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        glClearColor(0.1, 0.15, 0.1, 0.3)
        # self.image = cv2.imread("cat.png", cv2.IMREAD_GRAYSCALE)
        # self.ori_img = cv2.imread("cat.png", cv2.IMREAD_UNCHANGED)
        # print(self.ori_img.shape)
        self.Bind(wx.EVT_PAINT, self.OnDraw)

        os.environ['PYOPENGL_PLATFORM'] = 'egl'

        
        # vertices = np.array([   # position          color
        #                     0.5, -0.5, 0.0,  1.0, 0.0, 0.0,   # right-bottom
        #                     -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,   # left-bottom
        #                     0.0,  0.5, 0.0,  0.0, 0.0, 1.0    # up
        #                     ])

        im0 = cv2.imread("cat_noise.png")
        im1 = cv2.imread("noise.png")
        #sub_im = ((im0-im1+255)/2.0).astype(np.uint8)
        print(im0.shape)
        height, width, _ = im0.shape

        # self.vertices = np.array([0.5, 0.5, 0,    1.0, 0.0, 0.0,   1.0, 1.0,
        #                      0.5,-0.5, 0,    0.0, 1.0, 0.0,   1.0, 0.0,
        #                     -0.5,-0.5, 0,    0.0, 0.0, 1.0,   0.0, 0.0,
        #                     -0.5, 0.5, 0,    1.0, 1.0, 0.0,   0.0, 1.0], dtype = np.float32)

        self.vertices = np.array([0.5, 0.5, 0,    1.0, 1.0, 1.0,   1.0, 1.0,
                             0.5,-0.5, 0,    1.0, 1.0, 1.0,   1.0, 0.0,
                            -0.5,-0.5, 0,    1.0, 1.0, 1.0,   0.0, 0.0,
                            -0.5, 0.5, 0,    1.0, 1.0, 1.0,   0.0, 1.0], dtype = np.float32)

        self.indices = np.array([0, 1, 3,
                            1, 2, 3], dtype = np.uint32)       

        VAO = glGenVertexArrays(1)
       
        VBO, EBO = glGenBuffers(2)
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(self.vertices), self.vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sys.getsizeof(self.indices), self.indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)
        self.shaderProgram = shader.Shader("./img.vs.glsl", "./img.fsv2.glsl")
        self.VAO = VAO
        self.VBO = VBO

        self.texture1 = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, im0)
        glGenerateMipmap(GL_TEXTURE_2D)

        self.texture2 = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture2)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, im1)
        glGenerateMipmap(GL_TEXTURE_2D)
        #glBindBuffer(GL_ARRAY_BUFFER, 0)
        #glBindVertexArray(0) 

    def OnDraw(self, event):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
    
        self.shaderProgram.use()
        glUniform1i(glGetUniformLocation(self.shaderProgram.shaderProgram, "texture1"), 0)
        glUniform1i(glGetUniformLocation(self.shaderProgram.shaderProgram, "texture2"), 1)
        glBindVertexArray(self.VAO)
        
        # GL_POINTS
        # GL_LINE_STRIP
        # GL_LINE_LOOP
        # GL_LINES
        # ** GL_LINE_STRIP_ADJACENCY **
        # ** GL_LINES_ADJACENCY **
        # GL_TRIANGLE_STRIP
        # GL_TRIANGLE_FAN
        # GL_TRIANGLES
        # ** GL_TRIANGLE_STRIP_ADJACENCY **
        #glDrawArrays(GL_TRIANGLES, 0, 3)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture1)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture2)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        #glDrawArrays(GL_POINTS, 0, 3)
        glFlush()


        self.SwapBuffers()
        

class Window(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, parent=None, title=title, size=(1280, 720))
        # pnl = wx.Panel(self)
        # wx.StaticText(pnl, label="Hello World!")
        # self.SetBackgroundColour(wx.Colour( 194, 197, 204 ))
        self.canvas = OpenGLCanvas(self)
        # self.canvas.SetBackgroundColour(wx.Colour( 255, 255, 255 ))

class MyApp(wx.App):
    def OnInit(self):
        self.frame = Window("Hello World!")
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop() # infinitely display the window