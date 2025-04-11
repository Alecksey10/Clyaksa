from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor, QImage
import sys
import Xlib.display
from pymouse import PyMouseEvent


class Clickonacci(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        '''Print Fibonacci numbers when the left click is pressed.'''
        if button == 1:
            if press:
                print(x, y)
        else:  # Exit if any other mouse button used
            self.stop()

tmp_img = QImage()
tmp_img.load("./assets/img1.png")
tmp_img = tmp_img.convertToFormat(QImage.Format.Format_ARGB32)


print(tmp_img.size(), tmp_img.format())

for i in range(tmp_img.size().height()):
    for j in range(tmp_img.size().width()):
        color:QColor = tmp_img.pixelColor(j,i)
        color.setAlpha(100)
        tmp_img.setPixelColor
        tmp_img.setPixelColor(j,i,color)

class TrueClickThroughOverlay(QWidget):
    def __init__(self):
        super().__init__()

        # Настройки Qt
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 400)

        self.show()
        self.set_click_through()
        self.C = Clickonacci()
        self.C.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.setBrush(QColor(0, 0, 0, 100))
        # painter.setPen(Qt.NoPen)
        # painter.drawRect(self.rect())
        painter.drawImage(0,0, tmp_img)


    def set_click_through(self):
        """ Устанавливает InputShape для окна — X11-хак """
        from ctypes import CDLL, c_ulong, c_int
        xlib = CDLL("libX11.so")
        xshape = CDLL("libXext.so")

        display = xlib.XOpenDisplay(None)
        wid = self.winId().__int__()

        xshape.XShapeCombineRectangles(
            display,           # Display*
            wid,               # Window
            2,                 # ShapeInput
            0, 0,              # x, y
            None,              # rectangles
            0,                 # n_rects
            0,                 # ShapeSet
            0                  # ordering
        )
        xlib.XFlush(display)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrueClickThroughOverlay()
    sys.exit(app.exec())







