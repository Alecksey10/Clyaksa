import time
from pynput import keyboard
import threading

import sys

sys.path.append(".")
from source.shortcats.shortcat_getter import ShortcatGetter
from source.shortcats.shortcat_listener import ShortcatListener


class ShortcatMatcher:

    @staticmethod
    def normalize_key(key: str) -> str:
        """ Приводит ключ к нормальному виду: нижний регистр, без суффиксов """
        key = key.lower().replace('_l', '').replace('_r', '')
        replacements = {
            'control': 'ctrl',
            'return': 'enter',
            'escape': 'esc',
            'space': 'space',
            'command': 'cmd',
        }
        return replacements.get(key, key)
    @staticmethod
    def match(expected: list[str], current: list[str]) -> bool:
        """ Проверяет, совпадают ли две комбинации (без учёта порядка и регистра) """
        norm_expected = {ShortcatMatcher.normalize_key(k) for k in expected}
        norm_current = {ShortcatMatcher.normalize_key(k) for k in current}
        return norm_expected == norm_current


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])

    recorder = ShortcatGetter()


    def logic():
        print("комбинация записана, повтори:", recorder.keys, recorder.success)

        def on_keys_updated(keys):
            
            if(ShortcatMatcher.match(expected=recorder.keys, current=keys)):
                print("КЛАВИШИ СОШЛИСЬ", keys)
            pass

        listener = ShortcatListener(on_keys_updated)
        listener.start() 
        
    recorder.combination_recording_done_signal.connect(lambda: logic())
    recorder.show()

    app.exec()
