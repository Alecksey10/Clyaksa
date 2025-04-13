

import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QPushButton, QHBoxLayout

class CommandsExecutorView(QWidget):
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
        self.spinBox = QDoubleSpinBox()
        self.spinBox.setRange(0, 10000)  # Устанавливаем диапазон от 0 до 10000 мс
        self.spinBox.setSingleStep(10)   # Устанавливаем шаг изменения на 10
        self.spinBox.setDecimals(1)       # Устанавливаем одно десятичное
        self.spinBox.setValue(23)
        layout.addWidget(self.spinBox)

        # Кнопки
        self.startButton = QPushButton('Start')
        self.stopButton = QPushButton('Stop')

        # Связываем кнопки с методами
        self.startButton.clicked.connect(self.start_action)
        self.stopButton.clicked.connect(self.stop_action)

        # Располагаем кнопки в горизонтальном слое
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.startButton)
        buttonLayout.addWidget(self.stopButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def start_action(self):
        # Получаем значение из SpinBox
        delay = self.spinBox.value()
        print(f'Starting action with a delay of {delay} ms')
        # Здесь вы можете добавлять логику, которая будет выполняться с задержкой

    def stop_action(self):
        print('Action stopped')
        # Здесь вы можете добавить логику для остановки действия


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CommandsExecutorView()
    ex.show()
    sys.exit(app.exec())