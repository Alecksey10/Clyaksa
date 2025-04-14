import time
from pynput import keyboard
import threading

class ShortcatListener:
    #TODO баг, почему-то запоминает команды (SHIFT, например) и никак не выключает их. Походу, случается при одновременном нажатии клавишь. 
    def __init__(self, on_keys_updated=None):
        """
        :param on_keys_updated: функция, вызываемая при каждом изменении набора клавиш.
        """
        self._listener = None
        self._pressed_keys = set()
        self._on_keys_updated = on_keys_updated or (lambda keys: None)
        self._lock = threading.Lock()

    def start(self):
        """Запускает слушатель в отдельном потоке"""
        if self._listener is not None:
            return  # уже запущен

        def on_press(key):
            if(key == keyboard.Key.shift):
                return
            with self._lock:
                if key not in self._pressed_keys:
                    self._pressed_keys.add(key)
                    self._on_keys_updated(self._get_keys())

        def on_release(key):
            if(key == keyboard.Key.shift):
                return
            with self._lock:
                if key in self._pressed_keys:
                    self._pressed_keys.remove(key)
                    self._on_keys_updated(self._get_keys())

        self._listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        threading.Thread(target=self._listener.start, daemon=True).start()

    def stop(self):
        """Останавливает слушатель"""
        if self._listener:
            self._listener.stop()
            self._listener = None
            with self._lock:
                self._pressed_keys.clear()

    def _get_keys(self) -> list[str]:
        """Возвращает текущие зажатые клавиши в виде строк"""
        result = [self._key_to_string(k) for k in self._pressed_keys]
        return result

    def get_concurrent_keys(self) -> list[str]:
        """Возвращает текущие зажатые клавиши в виде строк"""
        result = [self._key_to_string(k) for k in self._pressed_keys]
        return result

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

def main():
    listener:ShortcatListener = None
    def on_keys_updated(keys):
        print(keys)
        pass
    listener = ShortcatListener(on_keys_updated)
    listener.start() 

    while True:
        pass

if __name__=="__main__":
    main()