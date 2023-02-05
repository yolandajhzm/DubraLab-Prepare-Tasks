from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QMainWindow, QGridLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
import cv2

# imgs = cv2.imread("cat.png", cv2.IMREAD_GRAYSCALE)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World!")
        self.setFixedSize(500, 500)

class DisplayImageWindow(QWidget):
    # def __init__(self):
    #     super().__init__()
    #     self.setWindowTitle("Hello World!")
    #     self.convert = QImage(imgs, imgs.shape[1], imgs.shape[0], imgs.strides[0], QImage.Format.Format_BGR888)
    #     self.frame = QLabel()
    #     self.frame.setPixmap(QPixmap.fromImage(self.convert))

    #     self.layout = QHBoxLayout(self)
    #     self.layout.addWidget(self.frame)

    #     self.show()
    def __init__(self):
        super(DisplayImageWindow, self).__init__()
        img = cv2.imread('cat.png', cv2.IMREAD_GRAYSCALE)
        self.convert = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format.Format_Grayscale8)
        self.frame = QLabel()
        self.frame.setPixmap(QPixmap.fromImage(self.convert))
        
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.frame)



if __name__ == "__main__":
    app = QApplication([])
    
    # background window
    main_window = MainWindow()
    
    central_widget = QWidget()
    main_layout = QGridLayout()
    central_widget.setLayout(main_layout)
    main_window.setCentralWidget(central_widget)
    
    display_image_widget = DisplayImageWindow()
    main_layout.addWidget(display_image_widget, 0, 0)
   
    main_window.show()
    app.exec()
    # app = QApplication([])
    # window = MainWindow()
    # app.exec()


# cite: stackoverflow
# import sys
# from PyQt6 import QtCore, QtWidgets, QtOpenGLWidgets, QtGui
# from OpenGL.GL import *

# class Window(QtWidgets.QWidget):
#     def __init__(self):
#         super(Window, self).__init__()
#         self.glWidget = GLWidget()
#         mainLayout = QtWidgets.QHBoxLayout()
#         mainLayout.addWidget(self.glWidget)
#         mainLayout.setContentsMargins(0,0,0,0)
#         self.setLayout(mainLayout)
#         self.setWindowTitle("Biovis")

# class GLWidget(QtOpenGLWidgets.QOpenGLWidget):
#     def __init__(self, parent=None):
#         super(GLWidget, self).__init__(parent)

#     def minimumSizeHint(self):
#         return QtCore.QSize(200, 200)

#     def sizeHint(self):
#         return QtCore.QSize(400, 400)

#     def initializeGL(self):
#         glClearColor(1, 0, 0, 1)

#     def paintGL(self):
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         glBegin(GL_TRIANGLES)
#         glVertex(-1, -1, 0)
#         glVertex(0, 1, 0)
#         glVertex(1, -1, 0)
#         glEnd()

#     def resizeGL(self, width, height):
#         glMatrixMode(GL_PROJECTION)
#         glLoadIdentity()
#         glViewport(0, 0, width, height)
#         glOrtho(-1, 1, -1, 1, -1, 1)
#         glMatrixMode(GL_MODELVIEW)
#         glLoadIdentity()

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec())
