from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QMainWindow, QGridLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
import cv2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World!")
        self.setFixedSize(500, 500)

class DisplayImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Hello World!")

        # convert image to numpy arrays 
        # 8 and 16 bits？pixel 8bit: 0-255
        # flag = cv2.IMREAD_GRAYSCALE default 8 bits
        # 0 for grayscale, 1 for color, -1 for unchanged
        img = cv2.imread('cat.png', 0)
        print(img.shape)
        print(img.strides)
        # img16bit = img.astype('uint16')
        # img = cv2.imread('cat.png', cv2.IMREAD_ANYDEPTH)
        # Img-data, width, height, bytesPerLine
        self.convert = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format.Format_Grayscale8)
        # self.convert = QImage(img16bit, img16bit.shape[1], img16bit.shape[0], img16bit.strides[0], QImage.Format.Format_Grayscale16)

        # QLabel displays non-editable text or image, or a movie of animated GIF
        self.frame = QLabel()
        self.frame.setPixmap(QPixmap.fromImage(self.convert))
        
        # QHBoxLayout line up widgets horizontally and vertically
        # self.layout = QHBoxLayout(self)
        # self.layout.addWidget(self.frame)



if __name__ == "__main__":
    app = QApplication([])
    
    # background window
    main_window = MainWindow()
    
    # MainWindow has fixed layout, so we should add central widget here
    # widget add layout AND layout add widget
    central_widget = QWidget()
    main_layout = QHBoxLayout()
    display_image_widget = DisplayImageWindow()

    main_layout.addWidget(display_image_widget.frame)
    central_widget.setLayout(main_layout)

    
    # if we set central widget as display_image-widget.frame, there won't be white space around the image
    main_window.setCentralWidget(central_widget)
   
    main_window.show()
    app.exec()
 

