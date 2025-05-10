from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor, QImage
import sys

from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QMimeData, Signal, QPoint
from PySide6.QtGui import QDrag, QMoveEvent

# class Clickonacci(PyMouseEvent):
#     def __init__(self):
#         PyMouseEvent.__init__(self)

#     def click(self, x, y, button, press):
#         '''Print Fibonacci numbers when the left click is pressed.'''
#         if button == 1:
#             if press:
#                 print(x, y)
#         else:  # Exit if any other mouse button used
#             self.stop()

# tmp_img = QImage()
# tmp_img.load("./assets/img1.png")
# tmp_img = tmp_img.convertToFormat(QImage.Format.Format_ARGB32)


# print(tmp_img.size(), tmp_img.format())

# # for i in range(tmp_img.size().height()):
# #     for j in range(tmp_img.size().width()):
# #         color:QColor = tmp_img.pixelColor(j,i)
# #         color.setAlpha(100)
# #         tmp_img.setPixelColor
# #         tmp_img.setPixelColor(j,i,color)




class ImageVizualizer(QWidget):
    position_changed_signal = Signal()
    def __init__(self, img:QImage=None):
        super().__init__()
        self.__b_blick_through = False
        self.__b_drag_and_drop = True
        self.__always_on_top = True
        self.opacity = 1.0
        self.pos_before_hide:QPoint = None
        if(img==None):
            self.img = QImage()
        else:
            self.img = img
        self._build_gui()

        self._dragging_currently_active = False
        self._drag_position = None
        self.set_image(img)

    def set_image(self, image:QImage):
        if not image or image.isNull():
            self.img = image
            self.resize(50, 50)
            self.update() 
            return
        self.img = image
        self.resize(image.width(), image.height())
        self.update()  # Перерисовать

    def _build_gui(self):
        # Настройки Qt
        self.setWindowFlags(
            # Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 400)

        self.show()
        # self.set_click_through(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        painter.setOpacity(self.opacity)  # <-- глобальная прозрачность
        if not self.img or self.img.isNull():
            pass
        else:
            painter.drawImage(0, 0, self.img)
    
    @property
    def click_through(self):
        
        """ X11 """
        return self.__b_blick_through
    
    @click_through.setter
    def click_through(self, value:bool):
        
        if(self.__b_blick_through==value):
            return
        self.__b_blick_through = value
        from ctypes import CDLL, c_ulong, c_int, POINTER, Structure
        from ctypes.util import find_library

        # Загрузка библиотек X11 и Xext
        xlib = CDLL(find_library("X11"))
        xext = CDLL(find_library("Xext"))

        # Константы
        ShapeInput = 2
        ShapeBounding = 0
        ShapeSet = 0
        ShapeRectangles = 0

        class XRectangle(Structure):
            _fields_ = [("x", c_int), ("y", c_int), ("width", c_int), ("height", c_int)]

        display = xlib.XOpenDisplay(None)
        if not display:
            print("Не удалось открыть X дисплей")
            return

        wid = self.winId().__int__()

        if self.__b_blick_through:
            # Убираем input-форму — окно становится "прозрачным" для событий
            xext.XShapeCombineRectangles(
                display,
                wid,
                ShapeInput,
                0, 0,
                None,
                0,
                ShapeSet,
                0
            )
        else:
            # Восстанавливаем input-форму на весь виджет
            width = self.width()
            height = self.height()
            rect = XRectangle(0, 0, width, height)
            xext.XShapeCombineRectangles(
                display,
                wid,
                ShapeInput,
                0, 0,
                POINTER(XRectangle)(rect),
                1,
                ShapeSet,
                0
            )

        xlib.XFlush(display)
    
    @property
    def drag_and_drop(self):
        return self.__b_drag_and_drop

    @drag_and_drop.setter
    def drag_and_drop(self, value:bool):
        self.__b_drag_and_drop = value

    @property
    def always_on_top(self):
        return self.__always_on_top
    
    @always_on_top.setter
    def always_on_top(self, value):
        if(self.__always_on_top==value):
            return
        
        self.__always_on_top = value
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, self.__always_on_top)
        
        self.repaint()
        

    def mousePressEvent(self, event):
        if(not self.__b_drag_and_drop):
            return
        
        if event.button() == Qt.LeftButton:
            # drag = QDrag(self)
            # mime_data = QMimeData()
            # mime_data.setText(self.objectName())
            # drag.setMimeData(mime_data)
            # drag.exec(Qt.MoveAction)

            self._dragging_currently_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if(not self.__b_drag_and_drop):
            return
        
        if self._dragging_currently_active and event.buttons() & Qt.LeftButton:
            new_pos = event.globalPosition().toPoint() - self._drag_position
            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging_currently_active = False
        event.accept()

    def moveEvent(self, event: QMoveEvent):
        super().moveEvent(event)     # важно вызывать родительский метод
        self.position_changed_signal.emit()

    def get_internal_pos(self) -> QPoint:
        return self.mapToGlobal(self.contentsRect().topLeft())

    def hide(self):
        self.pos_before_hide = self.pos()
        return super().hide()
    
    def show(self):
        
        result = super().show()
        if(self.pos_before_hide):
            if(self.pos_before_hide!=self.pos()):
                self.move(self.pos_before_hide)
        return result
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageVizualizer(QImage())
    window.drag_and_drop  = True
    window.click_through = False
    # window.always_on_top = False
    window.opacity = 0.5

    # window.show()
    def position_changed_handler():
        print(window.get_internal_pos())
        pass

    window.position_changed_signal.connect(position_changed_handler)
    # window2 = ImageVizualizer()
    # window2.drag_and_drop  = True
    # window2.click_through = True
    # window2.always_on_top = True
    # window2.show()
    sys.exit(app.exec())







