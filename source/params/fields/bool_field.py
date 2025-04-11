import random
from source.params.fields.field import FieldStricts
from source.params.fields.display_types import DisplayTypes


class BoolField(FieldStricts):
    
    def __init__(self, strcits_dict:dict=None, *args, **kwargs):
        if(strcits_dict == None):
            strcits_dict = {}
        
        self.default =  strcits_dict.get("default", False)
        self.name = strcits_dict.get("name", f"{random.randint(0,1000000)}")
        self.order = -1
        self.display_type = strcits_dict.get("display_type", DisplayTypes.CheckBox)
    
    def validate(self, value, *args, **kwargs):
        if(isinstance(value, bool)):
            return True
        return False
