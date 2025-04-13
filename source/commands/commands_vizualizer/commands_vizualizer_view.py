from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QDoubleSpinBox, QLabel, QHBoxLayout, QGridLayout
)
from PySide6.QtCore import Qt, Signal
import sys

sys.path.append(".")
from source.widgets.image_visualizer import ImageVizualizer


class CommandsVizualizerView(QWidget):
    params_updated_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Основной вертикальный layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)


        # Заглушка под display_widget
        # self.display_widget_layout = QVBoxLayout()
        # main_layout.addLayout(self.display_widget_layout)

        
        # Чекбокс: drag&drop
        self.drag_and_drop_checkbox = QCheckBox("режим drag and drop")
        self.drag_and_drop_checkbox.checkStateChanged.connect(lambda x: self.params_updated_signal.emit())
        # self.display_widget:ImageVizualizer = ImageVizualizer()
        main_layout.addWidget(self.drag_and_drop_checkbox)

        # Чекбокс: отдельное окно
        self.separate_window_checkbox = QCheckBox("отдельное окно")
        self.separate_window_checkbox.checkStateChanged.connect(lambda x: self.params_updated_signal.emit())
        main_layout.addWidget(self.separate_window_checkbox)

        # Спинбокс: от -180 до 180
        spinbox_layout = QHBoxLayout()
        spinbox_layout.addWidget(QLabel("угол:"))
        self.angle_spinbox = QDoubleSpinBox()
        self.angle_spinbox.setRange(-180.0, 180.0)
        self.angle_spinbox.setValue(0)
        self.angle_spinbox.setSingleStep(1.0)
        self.angle_spinbox.setDecimals(2)
        self.angle_spinbox.valueChanged.connect(lambda x: self.params_updated_signal.emit())
        spinbox_layout.addWidget(self.angle_spinbox)
        main_layout.addLayout(spinbox_layout)

        # масштабирование
        spinbox_layout = QHBoxLayout()
        spinbox_layout.addWidget(QLabel("масштабирование:"))
        self.scale_spinbox = QDoubleSpinBox()
        self.scale_spinbox.setRange(0, 10)
        self.scale_spinbox.setValue(1)
        self.scale_spinbox.setSingleStep(0.001)
        self.scale_spinbox.setDecimals(3)
        self.scale_spinbox.valueChanged.connect(lambda x: self.params_updated_signal.emit())
        spinbox_layout.addWidget(self.scale_spinbox)
        main_layout.addLayout(spinbox_layout)

        # Спинбокс: от 0 до 255
        spinbox_layout = QHBoxLayout()
        spinbox_layout.addWidget(QLabel("прозрачность:"))
        self.alpha_spinbox = QDoubleSpinBox()
        self.alpha_spinbox.setRange(0, 255)
        self.alpha_spinbox.setValue(255)
        self.alpha_spinbox.setSingleStep(1.0)
        self.alpha_spinbox.valueChanged.connect(lambda x: self.params_updated_signal.emit())
        spinbox_layout.addWidget(self.alpha_spinbox)
        main_layout.addLayout(spinbox_layout)

        # Чекбокс: подсвечивать checkpoint точки
        self.highlight_checkpoints_checkbox = QCheckBox("подсвечивать checkpoint точки")
        self.highlight_checkpoints_checkbox.checkStateChanged.connect(lambda x: self.params_updated_signal.emit())
        main_layout.addWidget(self.highlight_checkpoints_checkbox)

        # Чекбокс: подсвечивать пройденные точки
        self.highlight_passed_checkbox = QCheckBox("подсвечивать пройденные точки")
        self.highlight_passed_checkbox.checkStateChanged.connect(lambda x: self.params_updated_signal.emit())
        main_layout.addWidget(self.highlight_passed_checkbox)

        # Чекбокс: пропускать клики
        self.click_through_passed_checkbox = QCheckBox("кликать насквозь (фича доступна не везде)")
        self.click_through_passed_checkbox.checkStateChanged.connect(lambda x: self.params_updated_signal.emit())
        main_layout.addWidget(self.click_through_passed_checkbox)


        # coordinates_layout
        # self.coordinates_layout = QGridLayout()
        self.coordinates_label = QLabel("empty")

        # self.coordinates_layout.addWidget(self.coordinates_label, 0, 0)
        main_layout.addWidget(self.coordinates_label)

    def update_transform_shift(self, x, y):
        self.coordinates_label.setText(f"Сдвиг координат x:{x:>5} y:{y:>5}")



    # def set_display_widget(self, wgt:ImageVizualizer):
    #     #очстим виджет
    #     while self.display_widget_layout.count():
    #         item = self.display_widget_layout.takeAt(0)

    #         widget = item.widget()
    #         if widget is not None:
    #             widget.setParent(None)
    #             widget.deleteLater()
        
    #     self.display_widget = wgt
    




if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = CommandsVizualizerView()
    window.setWindowTitle("Контролы")
    window.resize(300, 300)
    window.show()

    display_window = ImageVizualizer()
    display_window.drag_and_drop  = True
    display_window.click_through = False
    # display_window.always_on_top = False
    display_window.opacity = 0.5


    # window.set_display_widget(display_window)

    sys.exit(app.exec())

