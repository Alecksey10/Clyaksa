from source.commands.click_mouse import ClickMouse
from source.commands.command_base import CommandBase
from source.commands.move_mouse_global import MoveMouseGlobal
from source.commands.move_mouse_relative import MoveMouseRelative
from source.commands.press_mouse import PressMouse
from source.commands.release_mouse import ReleaseMouse

import math
import time
import threading
from pynput import mouse
from pynput.mouse import Controller, Button
from pynput import keyboard

class CommandsExecutor():
    def __init__(self):
        self.mouse_ctl = Controller()

    def execute_command(self,command:CommandBase):
        if(isinstance(command,ClickMouse)):
            self.mouse_ctl.click(command.button)

        elif(isinstance(command,MoveMouseGlobal)):
            self.mouse_ctl.position = (command.x, command.y)

        elif(isinstance(command,MoveMouseRelative)):
            self.mouse_ctl.move(command.x, command.y)

        elif(isinstance(command,PressMouse)):
            self.mouse_ctl.press(command.button)

        elif(isinstance(command,ReleaseMouse)):
            self.mouse_ctl.release(command.button)