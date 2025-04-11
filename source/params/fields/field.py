

import abc
import sys
from source.params.fields.display_types import DisplayTypes


class FieldStricts(abc.ABC):


    @abc.abstractmethod
    def __init__(self, strcits_dict:dict=None, *args, **kwargs):
        self.default= None
        self.display_type:DisplayTypes = None
        self.name:str = ""
        self.order:int=-1
        pass

    @abc.abstractmethod
    def validate(self, value, *args, **kwargs):
        pass
