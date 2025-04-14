

import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QPushButton, QGridLayout

import sys
sys.path.append(".")
from source.commands.commands_iterator.commands_iterator import CommandsIterator
from source.shortcats.shortcat_getter import ShortcatGetter
from PySide6.QtCore import Signal

class CommandsExecutorView(QWidget):
    
    params_changed_signal = Signal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Delay Command Widget')

        layout = QVBoxLayout()

        # QLabel для описания
        self.label = QLabel('Введите задержку (в миллисекундах):')
        layout.addWidget(self.label)

        # QDoubleSpinBox для ввода времени задержки
        self.deltatime_spinbox = QDoubleSpinBox()
        self.deltatime_spinbox.setRange(0, 10000)  # Устанавливаем диапазон от 0 до 10000 мс
        self.deltatime_spinbox.setSingleStep(10)   # Устанавливаем шаг изменения на 10
        self.deltatime_spinbox.setDecimals(1)       # Устанавливаем одно десятичное
        self.deltatime_spinbox.setValue(23)
        self.deltatime_spinbox.valueChanged.connect(lambda value:self.params_changed_signal.emit())
        layout.addWidget(self.deltatime_spinbox)

        # Кнопки
        # self.startButton = QPushButton('Start')
        # self.stopButton = QPushButton('Stop')

        # Связываем кнопки с методами
        # self.startButton.clicked.connect(self.start)
        # self.startButton.clicked.connect(self.resume)
        # self.stopButton.clicked.connect(self.stop)

        # Располагаем кнопки в горизонтальном слое
        self.commands_layout = QGridLayout()
        shortcat_start_getter_label = QLabel("Начать")
        self.shortcat_start_getter = ShortcatGetter()
        self.shortcat_start_getter.set_keys(set(["Ctrl", "A"]))

        shortcat_resume_getter_label = QLabel("Продолжить")
        self.shortcat_resume_getter = ShortcatGetter()
        self.shortcat_resume_getter.set_keys(set(["Ctrl", "R"]))

        shortcat_stop_getter_label = QLabel("Остановить")
        self.shortcat_stop_getter = ShortcatGetter()
        self.shortcat_stop_getter.set_keys(set(["Ctrl", "S"]))


        # buttonLayout.addWidget(self.startButton)
        # buttonLayout.addWidget(self.stopButton)
        
        self.commands_layout.addWidget(shortcat_start_getter_label)
        self.commands_layout.addWidget(self.shortcat_start_getter)

        self.commands_layout.addWidget(shortcat_resume_getter_label)
        self.commands_layout.addWidget(self.shortcat_resume_getter)

        self.commands_layout.addWidget(shortcat_stop_getter_label)
        self.commands_layout.addWidget(self.shortcat_stop_getter)


        layout.addLayout(self.commands_layout)

        self.setLayout(layout)


    # def start(self):
    #     # Получаем значение из SpinBox
    #     delay = self.spinBox.value()
    #     print(f'Starting action with a delay of {delay} ms')
    #     # Здесь вы можете добавлять логику, которая будет выполняться с задержкой
    
    # def resume(self):
    #     # Получаем значение из SpinBox
    #     delay = self.spinBox.value()
    #     print(f'Starting action with a delay of {delay} ms')
    #     # Здесь вы можете добавлять логику, которая будет выполняться с задержкой

    # def stop(self):
    #     print('Action stopped')
    #     # Здесь вы можете добавить логику для остановки действия


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CommandsExecutorView()
    ex.show()
    sys.exit(app.exec())