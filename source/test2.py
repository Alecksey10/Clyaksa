import math
import time
import threading
from pynput import mouse
from pynput.mouse import Controller, Button
from pynput import keyboard

mouse_ctl = Controller()
drawing = False
stop_requested = False

def draw_circle(center_x, center_y, radius=50, steps=100, duration=1.0):
    global drawing, stop_requested

    drawing = True
    stop_requested = False

    interval = duration / steps
    mouse_ctl.position = (center_x + radius, center_y)
    mouse_ctl.press(Button.left)

    for i in range(steps + 1):
        if stop_requested:
            print("Рисование прервано.")
            break
        angle = 2 * math.pi * i / steps
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        mouse_ctl.position = (x, y)
        time.sleep(interval)

    mouse_ctl.release(Button.left)
    drawing = False

COMBO = {keyboard.Key.ctrl_l, keyboard.KeyCode(char='a')}
current_keys = set()

def on_press(key):
    global drawing, stop_requested
    current_keys.add(key)
    if all(k in current_keys for k in COMBO):
        x, y = mouse_ctl.position
        if drawing:
            stop_requested = True
        else:
            time.sleep(0.4)
            print(f"Старт рисования окружности в точке ({x}, {y})")
            threading.Thread(target=draw_circle, args=(x, y), daemon=True).start()

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
print("Слушаю горячие клавиши... (Esc — выход)")
listener.start()
listener.join()
