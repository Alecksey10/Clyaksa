import abc
from PySide6.QtCore import Signal


from source.commands.commands_generator.commands_generator_registry import CommandsGeneratorRegistry
from source.commands.commands_iterator.commands_iterator import CommandsIterator
from source.images.image_object_base import ImageObjectBase



class CommandsGeneratorBase(metaclass=CommandsGeneratorRegistry):
    params_updated_signal = Signal()


    def __init__(self):
        self.view = None
        self.model = None
    @abc.abstractmethod
    def process_image_object(self, img_object:ImageObjectBase):
        pass

    @abc.abstractmethod
    def get_commands_iterator(self) -> CommandsIterator:
        pass

    @classmethod
    @abc.abstractmethod
    def get_generator_name(cls) -> str:
        pass

