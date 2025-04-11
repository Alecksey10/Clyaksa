import pathlib
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QSpinBox, QDoubleSpinBox, QApplication
)
from PySide6.QtCore import QObject, Signal

class ParamsView(QWidget):
    params_updated_signal = Signal(str, object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
