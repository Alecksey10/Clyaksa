import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox
from PySide6.QtCore import Signal

class CommandsGeneratorViewBase(QWidget):

    generator_changed_signal = Signal()
    generate_btn_pressed_view_signal = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Создаем главный layout
        self.main_layout = QVBoxLayout(self)

        # Создаем layout для настроек
        self.generator_settings_layout = QVBoxLayout()

        # Пока добавляем только пустой layout для настроек
        # В дальнейшем сюда можно добавить другие виджеты для настроек
        self.generator_settings_layout.addWidget(QWidget())  # Это пустой виджет как пример

        # combobox для выбора типа генератора...
        self.combobox:QComboBox = QComboBox()
        self.combobox.currentIndexChanged.connect(lambda _: self.generator_changed_signal.emit())
        self.main_layout.addWidget(self.combobox)
        

        # Добавляем настройки в главный layout
        self.main_layout.addLayout(self.generator_settings_layout)

        # Создаем кнопку "Сгенерировать"
        generate_button = QPushButton("Сгенерировать", self)
        generate_button.pressed.connect(self.generate_btn_pressed_view_signal.emit)
        # Добавляем кнопку под layout с настройками
        self.main_layout.addWidget(generate_button)

        # Устанавливаем layout для виджета
        self.setLayout(self.main_layout)
        self.setWindowTitle("Пример виджета")
    def set_settings_widget(self, wgt:QWidget):
        #очстим виджет
        while self.generator_settings_layout.count():
            item = self.generator_settings_layout.takeAt(0)

            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self.generator_settings_layout.addWidget(wgt)

# Создание и запуск приложения

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = CommandsGeneratorViewBase()
    window.show()
    sys.exit(app.exec_())