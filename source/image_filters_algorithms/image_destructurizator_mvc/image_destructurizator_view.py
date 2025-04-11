
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QComboBox, QCheckBox, QApplication, QLabel, QSpinBox
)

from source.params_mvc.params_view import ParamsView

class ImageDestructurizatorView(QWidget):
    apply_filter_signal = Signal()
    def __init__(self,width, height,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.algorithm_container = QWidget() 
        self.combo = QComboBox()
        self.checkbox = QCheckBox("Применять по умолчанию")
        
        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 1950)
        self.width_spin.setSingleStep(1)
        self.width_spin.setValue(width)

        self.height_spin = QSpinBox()
        self.height_spin.setRange(0, 1950)
        self.height_spin.setSingleStep(1)
        self.height_spin.setValue(height)

        self.button = QPushButton("Применить фильтр")
        self.setLayout(QVBoxLayout())
        