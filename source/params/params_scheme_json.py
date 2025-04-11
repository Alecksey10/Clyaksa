
from typing import List
import sys
sys.path.append('.')
from source.params.params_obj import ParamsObj
import abc
from source.params.fields.field import FieldStricts
from source.params.params_scheme_base import ParamsSchemeBase
class ParamsSchemeJson(ParamsSchemeBase):


    def __init__(self, fields:List[FieldStricts]):
        self._params_obj:ParamsObj = ParamsObj()
        self.fields:List[FieldStricts] = fields

        for field in self.fields:
            if not self.try_set_param_by_name(name=field.name, value=field.default):
                raise Exception(f"cannot load values to scheme key:{field.name}, value:{field.default}")    




    def get_param_by_name(self, name:str):
        return getattr(self._params_obj, name)

    
        

    