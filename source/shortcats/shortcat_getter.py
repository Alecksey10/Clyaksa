from typing import List, Set
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from pynput import keyboard
import threading


from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from pynput import keyboard
import threading

class ShortcatGetter(QWidget):
    # TODO добавить нормализацию команд (сортировка)
    # Добавить прокси для комманд? а то вдруг кроссплатформенности нет
    # Добавить сортировку для листов команд? а то они перемешиваются при отображении
    '''Класс почти полностью написан нейронкой, но доведён до работоспособности, одурманящей ленивого '''
    combination_recording_done_signal = Signal()  # Сигнал с финальной комбинацией
    combination_recording_started_signal = Signal()  # Сигнал о начале записи (то есть желательно отключить другие listeners)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Комбинация горячих клавиш")
        # self.setFixedSize(300, 140)

        self.label = QLabel("Нажмите 'Записать комбинацию'")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Записать комбинацию")
        self.button.clicked.connect(self._toggle_recording)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self._recording = False
        self._listener = None
        self._pressed_keys = set()
        self._final_keys = []

        self.success = False
        self.keys = []

    def _toggle_recording(self):
        if self._recording:
            self.cancel_recording()
        else:
            self.start_recording()

    def start_recording(self):
        if self._recording:
            return
        self._recording = True
        self.success = False
        self.keys = []
        self._pressed_keys.clear()
        self._final_keys.clear()
        self.label.setText("Зажмите клавиши...")
        self.button.setText("Остановить запись")

        self.combination_recording_started_signal.emit()
        thread = threading.Thread(target=self._record_keys, daemon=True)
        thread.start()
        
    def is_recording(self):
        return self._recording
    
    def cancel_recording(self):
        """ Отмена записи — можно вызывать извне """
        if(not self._recording):
            return
        if self._listener:
            self._listener.stop()
        self._recording = False
        self.label.setText("Запись отменена")
        self.button.setText("Записать комбинацию")
        self._pressed_keys.clear()
        self._final_keys.clear()
        self._emit_combination()

    def _record_keys(self):
        def on_press(key):
            self._pressed_keys.add(key)
            if key not in self._final_keys:
                self._final_keys.append(key)
            self._update_label()

            if len(self._pressed_keys) >= 3:
                self.success = True
                self._stop_listener()
                self._emit_combination()

        def on_release(key):
            self._pressed_keys.discard(key)
            if len(self._pressed_keys) == 0:
                if(len(self._final_keys)>0):
                    self.success = True
                self._stop_listener()
                self._emit_combination()

        self._listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self._listener.start()
        self._listener.join()

    def set_keys(self, keys:Set[str]):
        self._stop_listener()
        self._final_keys = list(keys)
        self.success = True
        self._emit_combination()

    def _stop_listener(self):
        if self._listener:
            self._listener.stop()
        self._recording = False
        self.button.setText("Записать комбинацию")

    def _update_label(self):
        keys_str = [self._key_to_string(k) for k in self._final_keys]
        self.label.setText(" + ".join(keys_str) if keys_str else "Ожидание нажатия...")

    def _emit_combination(self):
        self.keys = [self._key_to_string(k) for k in self._final_keys]
        self.label.setText("Комбинация: " + (" + ".join(self.keys) if self.keys else "пусто"))
        self.combination_recording_done_signal.emit()

    def _key_to_string(self, key):
        try:
            return key.char.upper()
        except AttributeError:
            name = str(key).split('.')[-1].replace('_l', '').replace('_r', '').upper()
            replacements = {
                'CTRL': 'Ctrl',
                'SHIFT': 'Shift',
                'ALT': 'Alt',
                'CMD': 'Cmd',
                'ESC': 'Esc',
                'ENTER': 'Enter',
                'SPACE': 'Space',
                'TAB': 'Tab',
            }
            return replacements.get(name, name.title())

    def isValid(self) -> bool:
        """ Была ли успешно записана комбинация (минимум 1 клавиша) """
        return len(self._final_keys) > 0

    # def getCombination(self) -> list[str]:
    #     """ Возвращает комбинацию клавиш в виде списка строк """
    #     return [self._key_to_string(k) for k in self._final_keys]
    


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    recorder = ShortcatGetter()
    recorder.set_keys(set(["Ctrl", "Alt", "B"]))

    def combination_recording_started_handler():
        print("Запись начата")

    def combination_recorded_handler():
        print("комбинация записана", recorder.keys, recorder.success)


    recorder.combination_recording_started_signal.connect(lambda: combination_recording_started_handler())
    recorder.combination_recording_done_signal.connect(lambda: combination_recorded_handler())
    recorder.show()

    app.exec()
