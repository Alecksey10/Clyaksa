
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QComboBox, QCheckBox, QApplication, QLabel, QSpinBox
)

from source.params_mvc.params_view import ParamsView

class ImageDestructurizatorView(QWidget):
    apply_filter_signal = Signal()
    apply_filter_to_pinned_signal = Signal()

    pinn_filtered_image_signal = Signal()
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

        self.button_pinn_filtered = QPushButton("Закрепить результат")
        self.button_pinn_filtered.clicked.connect(self.pinn_filtered_image_signal.emit)

        self.button = QPushButton("Применить фильтр")
        self.button.clicked.connect(self.apply_filter_signal.emit)
        
        self.button_pinned = QPushButton("Применить фильтр к закреплённой")
        self.button_pinned.clicked.connect(self.apply_filter_to_pinned_signal.emit)
        self.setLayout(QVBoxLayout())
        