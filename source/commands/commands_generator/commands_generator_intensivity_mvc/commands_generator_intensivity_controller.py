

import abc
from source.commands.commands_generator.commands_generator_base import CommandsGeneratorBase
from source.commands.commands_generator.commands_generator_intensivity_mvc.commands_generator_intensivity_model import CommandsGeneratorIntensivityModel
from source.commands.commands_generator.commands_generator_intensivity_mvc.commands_generator_intensivity_view import CommandsGeneratorIntensivityView
from source.images.image_object_base import ImageObjectBase


class CommandsGeneratorIntensivityController(CommandsGeneratorBase):
    
    def __init__(self):
        super().__init__()
        self.model = CommandsGeneratorIntensivityModel()
        self.view = CommandsGeneratorIntensivityView() 

    def process_image_object(self, img_object:ImageObjectBase):
        print("image processed at intensivity")
        pass

    def get_commands_iterator(self):
        print("commands generated at intensivity")
        pass

    @classmethod
    def get_generator_name(cls) -> str:
        return "intensivity commands generator"