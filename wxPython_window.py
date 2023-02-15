import wx
from wx import glcanvas
from OpenGL.GL import *


class OpenGLCanvas(wx.glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(680, 630))
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        glClearColor(0.1, 0.15, 0.1, 1.0)
        self.Bind(wx.EVT_PAINT, self.OnDraw)

    def OnDraw(self, event):
        glClear(GL_COLOR_BUFFER_BIT)
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


