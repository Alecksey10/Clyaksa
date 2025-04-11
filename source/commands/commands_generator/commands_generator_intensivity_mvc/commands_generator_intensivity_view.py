

import abc
import sys
sys.path.append('.')
from source.commands.commands_generator.commands_generator_base import CommandsGeneratorBase
from source.images.image_object_base import ImageObjectBase

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDoubleSpinBox, QCheckBox, QLabel
)
from PySide6.QtCore import Qt

class CommandsGeneratorIntensivityView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout(self)

        # 1. SpinBox: минимальное расстояние между точками (0.0–1000.0)
        self.min_distance_spin = QDoubleSpinBox()
        self.min_distance_spin.setRange(0.0, 1000.0)
        self.min_distance_spin.setSingleStep(0.1)
        self.min_distance_spin.setValue(10.0)
        self.min_distance_spin.setDecimals(2)
        layout.addLayout(self._with_label("Мин. расстояние:", self.min_distance_spin))

        # 2. Checkbox-заглушка
        self.checkpoints_checkbox = QCheckBox("генерировать checkpoints по возможности")
        layout.addWidget(self.checkpoints_checkbox)

        # 3. SpinBox: чувствительность к интенсивности (0.0–255.0)
        self.intensity_spin = QDoubleSpinBox()
        self.intensity_spin.setRange(0.0, 255.0)
        self.intensity_spin.setSingleStep(1.0)
        self.intensity_spin.setValue(50.0)
        self.intensity_spin.setDecimals(1)
        layout.addLayout(self._with_label("Порог интенсивности:", self.intensity_spin))

        # 4. Checkbox-заглушка (сократить серию команд click)
        self.trim_commands_checkbox = QCheckBox("Сокращать команды")
        layout.addWidget(self.trim_commands_checkbox)

        layout.addStretch()

    def _with_label(self, text: str, widget: QWidget) -> QHBoxLayout:
        hbox = QHBoxLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        label.setFixedWidth(160)
        hbox.addWidget(label)
        hbox.addWidget(widget)
        return hbox

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = CommandsGeneratorIntensivityView()
    w.setWindowTitle("Параметры детекции")
    w.resize(400, 200)
    w.show()
    sys.exit(app.exec())
