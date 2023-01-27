import wx


class Window(wx.Frame):
    def __init__(self, title):
        super().__init__(parent=None, title=title, size=(300, 200))
        pnl = wx.Panel(self)
        wx.StaticText(pnl, label="Hello World!")


        self.Show() # display the window


if __name__ == "__main__":
    app = wx.App()
    window = Window("Task 1") # window title
    app.MainLoop() # infinitely display the window