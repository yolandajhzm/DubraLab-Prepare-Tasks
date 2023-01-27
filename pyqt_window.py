from PyQt6.QtWidgets import QWidget, QApplication


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World!")
       # self.setGeometry(100, 100, 300, 300)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec()