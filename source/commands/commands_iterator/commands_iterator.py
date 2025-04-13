from typing import Iterable, List

from source.commands.command_base import CommandBase
from source.commands.click_mouse import ClickMouse


class CommandsIterator(Iterable):
    def __init__(self, commands:List[CommandBase], width:int=0, height:int=0):
        self.current = 0
        self.end = len(commands)
        self.commands = commands
        self.width = width
        self.height = height
        super().__init__()
    
    def __iter__(self):
        return self
    
    def restart(self):
        self.current = 0
    
    def get_all_click_mouse_commands(self) -> List[ClickMouse]:
        result = []
        for command in self:
            if(isinstance(command, ClickMouse)):
                result.append(command)
        return result
    
    def __next__(self):
        if(self.current<self.end):
            self.current+=1
            return self.commands[self.current-1]
        else:
            raise StopIteration
    
    def __len__(self):
        return len(self.commands)
