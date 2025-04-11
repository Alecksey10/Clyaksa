from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PySide6.QtGui import QPixmap, QImage, QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt, QPoint


class ImageObjectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scale_factor = 1.0
        self._last_mouse_pos = QPoint()
        self._drag_active = False

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setScaledContents(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.label)

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_area)

    def set_image(self, image: QImage):
        """Установить новое изображение"""
        self._qimage = image
        self.pixmap = QPixmap.fromImage(image)
        self.scale_factor = 1.0
        self._update_view()

    def _update_view(self):
        """Обновить масштабированное изображение"""
        if not hasattr(self, 'pixmap'):
            return

        scaled = self.pixmap.scaled(
            self.scale_factor * self.pixmap.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(scaled)

    def wheelEvent(self, event: QWheelEvent):
        """Обработка масштабирования колесиком мыши"""
        if not hasattr(self, 'pixmap'):
            return

        angle_delta = event.angleDelta().y()
        factor = 1.25 if angle_delta > 0 else 0.8

        self.scale_factor *= factor
        self.scale_factor = max(0.1, min(10.0, self.scale_factor))
        self._update_view()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._last_mouse_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_active:
            delta = event.globalPosition().toPoint() - self._last_mouse_pos
            self._last_mouse_pos = event.globalPosition().toPoint()
            self.scroll_area.horizontalScrollBar().setValue(
                self.scroll_area.horizontalScrollBar().value() - delta.x()
            )
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().value() - delta.y()
            )

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = False