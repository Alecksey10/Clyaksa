
import abc

import pynput


class CommandBase():
    def __init__(self):
        #вдруг пользователь нажмёт паузу..., надо будет найти самую ближайшую (пусть и в обратную сторону) команду, с которой можно будет начать снова. 
        self.is_checkpointable:bool
    
    def is_checkpointable_moment(self)->bool:
        return self.is_checkpointable
    
    def set_checkpointable(self, is_checkpointable:bool):
        self.is_checkpointable = is_checkpointable
    