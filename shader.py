from OpenGL.GL import *
import wx
from wx import glcanvas
from OpenGL.GL import *
import cv2
from OpenGL.GL import *
import numpy as np 
import shader as shader
import os
 
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
        self.image = cv2.imread("cat.png", cv2.IMREAD_GRAYSCALE)
        self.ori_img = cv2.imread("cat.png", cv2.IMREAD_UNCHANGED)
        print(self.ori_img.shape)
        self.Bind(wx.EVT_PAINT, self.OnDraw)

        os.environ['PYOPENGL_PLATFORM'] = 'egl'
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)
        
        vertices = np.array([   
                            0.5, -0.5, 0.0,  1.0, 0.0, 0.0,   # right-bottom
                            -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,   # left-bottom
                            0.0,  0.5, 0.0,  0.0, 0.0, 1.0    # up
                            ])
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, 8 * vertices.size, vertices, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 3, GL_DOUBLE, GL_FALSE, int(8 * 6), None)
        glEnableVertexArrayAttrib(VAO, 0)
        glVertexAttribPointer(1, 3, GL_DOUBLE, GL_FALSE, int(8 * 6), ctypes.c_void_p(8 * 3))
        glEnableVertexArrayAttrib(VAO, 1)
        self.shaderProgram = shader.Shader("./test.vs.glsl", "./test.fs.glsl")
        self.VAO = VAO
        self.VBO = VBO
        

    def OnDraw(self, event):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
    
        self.shaderProgram.use()
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
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