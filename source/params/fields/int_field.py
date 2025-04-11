import random
from source.params.fields.field import FieldStricts
from source.params.fields.display_types import DisplayTypes


class IntField(FieldStricts):
    
    def __init__(self, strcits_dict:dict=None, *args, **kwargs):
        if(strcits_dict == None):
            strcits_dict = {}
        
        self.default =  strcits_dict.get("default", 0)
        self.max = strcits_dict.get("max", 1000000)
        self.min = strcits_dict.get("min", -1000000)
        self.name = strcits_dict.get("name", f"{random.randint(0,1000000)}")
        self.step = strcits_dict.get("step", 1)
        self.order = -1
        self.display_type = strcits_dict.get("display_type", DisplayTypes.InputField)
    
    
    def validate(self, value, *args, **kwargs):
        if(not isinstance(value, int)):
            return False
        elif(value<self.min or value>self.max):
            return False
        else:
            return True