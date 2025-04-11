import random
from source.params.fields.field import FieldStricts
from source.params.fields.display_types import DisplayTypes


class ComboboxField(FieldStricts):
    
    def __init__(self, strcits_dict:dict=None, *args, **kwargs):
        if(strcits_dict == None):
            strcits_dict = {}
        
        self.default=strcits_dict.get("default","default, not setted")
        self.values = strcits_dict.get("values", [self.default,"default, not setted"+"222"])
        self.name = strcits_dict.get("name", f"{random.randint(0,1000000)}")
        self.order = -1
        self.display_type = strcits_dict.get("display_type", DisplayTypes.ComboBox)
    
    def validate(self, value, *args, **kwargs):
        if(not value in self.values):
            return False
        return True